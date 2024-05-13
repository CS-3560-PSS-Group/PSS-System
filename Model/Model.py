import json 
from datetime import datetime, timedelta

from Task.Task import Task, TransientTask, RecurringTask, AntiTask


from .CheckOverlap import check_overlap, can_apply_anti_task

# Not even god can help me refactor this code


class Model:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
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

    # assign anti_task to a specific instance of a recurring task, returns false 
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


    def get_week_schedule(self, week_start_date):
        pass

    
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
