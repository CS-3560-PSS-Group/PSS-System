import json 
from datetime import datetime, timedelta

from Task.Task import Task, TransientTask, RecurringTask, AntiTask, Event


from .CheckOverlap import check_overlap, can_apply_anti_task, get_datetime_from_date, get_datetime_from_datetime, get_datetime_from_dur

# checks if two ranges overlap. start and end are both inclusive bounds. 
def do_datetime_ranges_overap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    return (start1 <= end2) and (end1 >= start2)

def get_date_and_time_from_datetime(dt):
    # Extract date components
    date_int = int(dt.strftime("%Y%m%d"))

    # Calculate time in decimal hours
    time_float = dt.hour + dt.minute / 60 + dt.second / 3600

    return date_int, time_float

class Model:
    def __init__(self):
        self.tasks: list[Task] = []

    # Add any kind of task. Can be Recurring, Transient, or Anti
    def add_task(self, task: Task):
        if type(task) == AntiTask:
            self.add_anti_task(task)
        else:
            # Attempts to create the task. Returns True if it fits the schedule, or False otherwise
            for existing_task in self.tasks:

                # raise eror if same name as existing task or anti-task
                if task.name == existing_task.name:
                    raise ValueError('Attempted to add task with duplicate name')
                elif type(existing_task) is RecurringTask:
                    for atask in existing_task.anti_tasks:
                        if task.name == atask.name:
                            raise ValueError('Attempted to add task with duplicate name')
                        
                # raise error if overlaps with existing task
                if check_overlap(existing_task, task):
                    raise ValueError('Task overlaps an existing task')

            self.tasks.append(task)
        return True

    # assign anti_task to first found compatible Recurring Task Object in Model
    # return True on success, LookupError on failure
    def add_anti_task(self, anti_task: AntiTask): 
        # iterate all tasks for recurring tasks
        for existing_task in self.tasks:
            if type(existing_task) is RecurringTask:
                # if anti-task has a corresponding RecurringTask instance, have them ref each other
                if can_apply_anti_task(anti_task, existing_task):
                    existing_task.add_anti_task(anti_task)
                    anti_task.reference_task(existing_task)
                    return True
                
        raise LookupError('Error: AntiTask does not apply to any existing recurring task')


    # this function will get all the Events that occur from the start_date to the end_date, exclusive. No specific times, just the whole day as a boundary.
    def get_events_within_timeframe(self, start_date: int, days: int) -> list[Event]:
        result = []

        start_datetime = get_datetime_from_date(start_date)
        end_datetime = start_datetime + timedelta(days = (days-1), hours = 23, minutes = 45)  # making inclusive end_datetime. this is the last timestamap of the timeframe.

        for task in self.tasks:
            if type(task) is TransientTask:
                begin = get_datetime_from_datetime(task.start_date, task.start_time)
                end = get_datetime_from_dur(begin, task.duration)

                if do_datetime_ranges_overap(start_datetime, end_datetime, begin, end): # this task happens during the timeframe
                    result.append(Event(task.start_date, task.start_time, task.duration, task))
            elif type(task) is RecurringTask:
                # this is the last occurrence of the recurring task. it is the datetime of the start of that occurrence 
                last_occurrence_start_datetime = get_datetime_from_datetime(task.end_date, task.start_time)   

                occurrence_start_datetime = get_datetime_from_datetime(task.start_date, task.start_time)

                while occurrence_start_datetime < end_datetime and occurrence_start_datetime <= last_occurrence_start_datetime:
                    occurrence_end_datetime = get_datetime_from_dur(occurrence_start_datetime, task.duration)

                    # if this occurrence happens during the timeframe
                    if do_datetime_ranges_overap(start_datetime, end_datetime, occurrence_start_datetime, occurrence_end_datetime):
                        # check if theres any anti-task affecting this occurrence. if there are none, then this can be added as an event.
                        # the specifications for the assignment requires that anti-task's start and end corresponds exactly with the recurring task, so this is an adequate check. 
                        if not any(get_datetime_from_datetime(anti_task.start_date, anti_task.start_time) == occurrence_start_datetime for anti_task in task.anti_tasks):   
                            occurrence_start_date, occurrence_start_time = get_date_and_time_from_datetime(occurrence_start_datetime)
                            result.append(Event(occurrence_start_date, occurrence_start_time, task.duration, task))
                        
                    occurrence_start_datetime = occurrence_start_datetime + timedelta(days=task.frequency)
        
        result.sort(key=lambda event: get_datetime_from_datetime(event.start_date, event.start_time))

        return result

    
    # returns recurring or transient task object by name
    def find_task_by_name(self, name: str) -> Task:
        for task in self.tasks:
            if task.name == name:
                return task
        return None
    

    # return list of RecurringTask objects in model
    def get_recurring_tasks(self):
        rec_list = list()
        for task in self.tasks:
            if type(task) is RecurringTask:
                rec_list.append(task)

        return rec_list
    

    # return list of TransientTask objects in model
    def get_transient_tasks(self): 
        tra_list = list()
        for task in self.tasks:
            if type(task) is TransientTask:
                tra_list.append(task)

        return tra_list


    # return list of AntiTask objects in model
    def get_anti_tasks(self):
        rec_list = self.get_recurring_tasks()
        at_list = list()

        # iterate through all recurring tasks in model, add their AntiTasks to at_list
        for task in rec_list:
            for a_task in task.anti_tasks:
                at_list.append(a_task)

        return at_list
    

    # function that dumps the whole schedule to JSON. in other words, this dumped JSON can be imported later, to restore the exact state of the system.
    def dump_full_schedule_to_json(self) -> str:
        return json.dumps([task.to_dict() for task in self.tasks], indent=2)
    

    # imports task list from valid json file
    def import_schedule_from_json(self, json_str: str):
        try:
            task_dict_list = json.loads(json_str)

            tasks_to_add = []

            # task_list is a list of Dictionaries. Each dict stores the attributes of a single task.
            for t in task_dict_list: 
                if "Frequency" in t:  # if this is a recurring task
                    tasks_to_add.append(RecurringTask(t["Name"], t["Type"], t["StartDate"], t["StartTime"], t["Duration"], t["EndDate"], t["Frequency"]))
                elif t["Type"] == "Cancellation":  # if this is an anti-task
                    tasks_to_add.append(AntiTask(t["Name"], t["Date"], t["StartTime"], t["Duration"]))
                else:  # otherwise, its a transient task
                    tasks_to_add.append(TransientTask(t["Name"], t["Type"], t["Date"], t["StartTime"], t["Duration"]))
        except:
            raise ValueError("JSON is not formatted properly")
        
        # sort tasks_to_add such that Recurring Tasks are first, AntiTasks are second, and Transient Tasks are last. 
        tasks_to_add.sort(key=lambda t: [RecurringTask, AntiTask, TransientTask].index(type(t)))

        tasks_backup = self.tasks.copy()
        try:
            # try and add all the tasks to the model. If it completes, then there were no issues
            for task in tasks_to_add:
                self.add_task(task)
        except: 
            # if theres an exception, restore the Model back to its previous state, and throw another exception for the calling function.
            self.tasks = tasks_backup
            raise ValueError("Tasks Overlap")
        

        # deletes a transient or recurring task object from Model
        # return True if successful, otherwise raises LookupError
        def delete_task(self, task_name: str):
            task = self.find_task_by_name(task_name)
            if task != None:
                self.tasks.remove(task)
                return True
            
            raise LookupError("Task with specified name does not exist in model")
        

        # edits a recurring or transient task object in Model
        # parameters: task_name (string), task (new task object to replace specified task)
        def edit_task(self, task_name: str, task: Task):

            # identify task to be edited and raise error if does not exist in Model
            target_task = self.find_task_by_name(task_name)
            if target_task == None:
                raise LookupError("Task with specified name does not exist in model")
            
            if not(type(target_task) is type(task)):
                raise TypeError("New task does not match existing type")
            
            if type(target_task) is RecurringTask and type(task) is RecurringTask:
                for atask in target_task.anti_tasks:
                    task.add_anti_task()


