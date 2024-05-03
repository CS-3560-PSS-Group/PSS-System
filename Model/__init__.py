from datetime import datetime

from ..Task import Event, Task, RecurringTask, TransientTask, AntiTask


def check_overlap(task1: Task, task2: Task):
    return False

def can_apply_anti_task(atask: AntiTask, rectask: RecurringTask):

    atask_start = get_datetime_from_date(atask.start_date)
    rectask_start = get_datetime_from_date(rectask.start_date)
    rectask_end = get_datetime_from_date(rectask.end_date)

    # handle daily recurring task
    if rectask.frequency == 1:

        # check if new anti-task falls within date and time restraints of recurring task
        if atask_start >= rectask_start and atask_start <= rectask_end:
            if atask.start_time == rectask.start_time and atask.duration == rectask.duration:

                # return False if identical anti-task exists
                for existing_atask in rectask.anti_tasks:
                    if existing_atask.start_date == atask.start_date:
                        return False
                    
                # else return True
                return True
    
    # handle weekly recurring task
    if rectask.frequency == 7:
        atask_day = get_day_of_week(atask.start_date)
        rectask_day = get_day_of_week(rectask.start_date)

        # check if anti-task falls within datetime constraints of recurring task, on the correct weekday
        if atask_day == rectask_day:
            if atask_start >= rectask_start and atask_start <= rectask_end:
                if atask.start_time == rectask.start_time and atask.duration == rectask.duration:
                   
                    # return False if identical anti-task exists
                    for existing_atask in rectask.anti_tasks:
                        if existing_atask.start_date == atask.start_date:
                            return False
                    
                    # else return True
                    return True

    # default to return False
    return False

# returns datetime object from integer date
def get_datetime_from_date(date):
    date_str = str(date)   # YYYYMMDD
    year = int(date_str[0:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return datetime(year, month, day)

# returns weekday from integer date
def get_day_of_week(date):
    date_obj = get_datetime_from_date(date)
    return date_obj.weekday()

"""
def do_times_overlap(start_time1, duration1, start_time2, duration2):
    # two times overlap IF (StartA <= EndB) and (EndA >= StartB)...
    return start_time1 <= start_time2 + duration2 and start_time1 + duration1 >= start_time2

def do_dates_overlap(start_date1, end_date1, start_date2, end_date2):
    return start_date1 <= end_date2 and end_date1 >= start_date2

# checks if recurring tasks overlap each other
def do_recurring_tasks_collide( task1: RecurringTask, task2: RecurringTask):
    num_daily = 0 # how many tasks occur daily. if both are daily, then 2. if only one is daily, and other is weekly, then num_daily = 1
    if task1.frequency == 1:
        num_daily+=1
    if task2.frequency == 1:
        num_daily+=1

    if num_daily == 0:  # weekly and weekly
        start_date_obj_1 = get_datetime_from_date(task1.start_date)
        start_date_obj_2 = get_datetime_from_date(task2.start_date)
        days_difference = abs((start_date_obj_2 - start_date_obj_1).days)

        if days_difference % 7 == 0:  # if these two occur on the same weekday
            latest_start_date = max(task1.start_date, task2.start_date)
            earliest_end_date = min(task1.end_date, task2.end_date)
            return latest_start_date <= earliest_end_date
        else:
            return False

    elif num_daily == 1:
        if task1.frequency != 1:  # i want task1 to be the one thats daily. if its task2, then swap them.
            task1, task2 = task2, task1
        

    elif num_daily == 2:
        pass
"""


class Model:
    def __init__(self):
        """
        self.recurring_tasks: list[RecurringTask] = []
        self.transient_tasks: list[TransientTask] = []
        self.anti_tasks: list[AntiTask] = []
        """
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        #A ttempts to create the task. Returns True if it fits the schedule, or False otherwise
        for existing_task in self.tasks:
            if check_overlap(existing_task, task):
                raise ValueError('New task overlaps with an existing task')
            
            """if ((task.frequency == 1 or existing_task.frequency == 1 or   # check if they land on the same day of the week
                    do_dates_overlap(task.start_date, task.end_date, existing_task.start_date, existing_task.end_date) and    # check the actual start and end date
                    do_times_overlap(task.start_time, task.duration, existing_task.start_time, existing_task.duration)):      # check the time of the events during the day
                
        
        for existing_task in self.transient_tasks:
            if self.do_recurring_and_transient_tasks_collide(task, existing_task):
                raise ValueError("New task overlaps with an existing task")"""

        self.tasks.append(task)
        return True
   
    """
    def add_transient_task(self, task: TransientTask ):
        for existing_task in self.recurring_tasks:
            if self.do_recurring_and_transient_tasks_collide(existing_task, task):
                raise ValueError("New task overlaps with an existing task")

        for existing_task in self.transient_tasks:
            if (task.start_date == existing_task.start_date and 
                    do_times_overlap(task.start_time, task.duration, existing_task.start_time, existing_task.duration)):
                raise ValueError("New task overlaps with an existing task")

        self.transient_tasks.append(task)

    def do_recurring_and_transient_tasks_collide(self, recurring_task: RecurringTask, transient_task: TransientTask):
        if (recurring_task.start_date <= transient_task.start_date <= recurring_task.end_date and  # if transient task is within the dates of the recurring task
                recurring_task.week_days[get_day_of_week(transient_task.start_date)] == True and  # if the transient task lands on a weekday that the recurring task is scheduled for
                do_times_overlap(transient_task.start_time, transient_task.duration, recurring_task.start_time, recurring_task.duration)):      # check the time of the events during the day
            # if they seem to collide, check to see if theres an anti task that frees this spot
            for anti_task in self.anti_tasks:
                if (anti_task.start_date == transient_task.start_date and # if transient task and anti task are on the same date, AND if transient task is within the anti task's time
                        transient_task.start_time >= anti_task.start_time and transient_task.start_time + transient_task.duration <= anti_task.start_time + anti_task.duration):
                    return False
            return True # True if no suitable anti task is found
        
        return False # False if no recurring task collides with transient task"""

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


    """
    def get_week_schedule(self, week_start_date):
        events = []
        for recurring_task in self.recurring_tasks:
            if recurring_task.start_date <= week_start_date <= recurring_task.end_date: # if this recurring task applies to this week

                for i in range(7): # for each day of the week
                    if recurring_task.week_days[i] == True:
                        e = Event(recurring_task.name, True, recurring_task.task_type, i, recurring_task.start_time, recurring_task.duration, 
                                  "Started on " + recurring_task.start_date + " with " + (-1) + " iterations left")   # TODO  FIX THIS 
                        events.append(e)
                        
        for anti_task in self.anti_tasks:
            week_start_date_obj = get_datetime_from_date(week_start_date)
            anti_task_start_date_obj = get_datetime_from_date(anti_task.start_date)
            if 0 <= (anti_task_start_date_obj - week_start_date_obj).days <= 6:


    def get_recurring_tasks():
        pass
    
    def get_transient_tasks(): 
        pass

    def get_anti_tasks():
        pass

    def is_task_valid():
        pass"""
    
