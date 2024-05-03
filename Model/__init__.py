from datetime import datetime, timedelta

from ..Task import Task, RecurringTask, TransientTask, AntiTask


def check_overlap(task1: Task, task2: Task):
    
    if type(task1) is TransientTask and type(task2) is TransientTask:
        return transient_datetimes_overlap(task1, task2)
    elif type(task1) is RecurringTask and type(task2) is RecurringTask:
        return recurring_tasks_overlap(task1, task2)
    elif type(task1) is RecurringTask and type(task2) is TransientTask:
        return diff_tasks_overlap(task1, task2)
    else:
        return diff_tasks_overlap(task2, task1)


# compare two transient tasks and return True if they overlap
def transient_datetimes_overlap(task1: TransientTask, task2: TransientTask):
    task1_start = get_datetime_from_datetime(task1.start_date, task1.start_time)
    task1_end = get_datetime_from_dur(task1_start, task1.duration)

    task2_start = get_datetime_from_datetime(task2.start_date, task2.start_time)
    task2_end = get_datetime_from_dur(task2_start, task2.duration)

    if task1_end <= task2_start or task1_start >= task2_end:
        return False
    else:
        return True


# compare two recurring tasks and return True if they overlap
def recurring_tasks_overlap(task1: RecurringTask, task2: RecurringTask):

    # start datetime & end datetime for the first instance of the task
    task1_start = get_datetime_from_datetime(task1.start_date, task1.start_time)
    task1_start_end = get_datetime_from_dur(task1_start, task1.duration)
    task1_weekday = task1_start.weekday

    # start datetime & end datetime for the last instance of the task
    if task1.frequency == 1:
        task1_end_date = get_datetime_from_datetime(task1.end_date, task1.start_time)
        task1_end_date_end = get_datetime_from_dur(task1_end_date, task1.duration)
    elif task1.frequency == 7:
        task1_end_date = get_datetime_from_datetime(task1.end_date, task1.start_time)
        
        # decrement end_date datetime by a day until it's the correct weekday
        while (task1_end_date.weekday != task1_weekday):
            task1_end_date -= timedelta(days=1)
        task1_end_date_end = get_datetime_from_dur(task1_end_date, task1.duration)

    # same structure as above but for task2
    task2_start = get_datetime_from_datetime(task2.start_date, task2.start_time)
    task2_start_end = get_datetime_from_dur(task2_start, task2.duration)
    task2_weekday = task2_start.weekday

    if task2.frequency == 1:
        task2_end_date = get_datetime_from_datetime(task2.end_date, task2.start_time)
        task2_end_date_end = get_datetime_from_dur(task2_end_date, task2.duration)
    elif task2.frequency == 7:
        task2_end_date = get_datetime_from_datetime(task2.end_date, task2.start_time)
        while (task2_end_date.weekday != task2_weekday):
            task2_end_date -= timedelta(days=1)
        task2_end_date_end = get_datetime_from_dur(task2_end_date, task2.duration)

    # if their dates never overlap, return False
    if task1_end_date_end <= task2_start or task1_start >= task2_end_date_end:
        return False
    
    # handle comparison for daily tasks
    elif task1.frequency == 1 and task2.frequency == 1:
        # assume matching dates to make accounting for tasks that span multiple days easier
        task1_start_modified = modify_date(task1_start, task2_start)
        task1_start_end_modified = get_datetime_from_dur(task1_start_modified, task1.duration)
        # if times never overlap, return False
        if task1_start_end_modified <= task2_start or task1_start_modified >= task2_start_end:
            return False
        
    # handle comparison for weekly tasks
    elif task1.frequency == 7 and task2.frequency == 7:
        # preserve starting weekday of task 1, assume matching week to make accounting for tasks that span multiple days easier
        task1_start_modified = modify_week(task1_start, task2_start)
        task1_start_end_modified = get_datetime_from_dur(task1_start_modified, task1.duration)
        # if times never overlap, return False
        if task1_start_end_modified <= task2_start or task1_start_modified >= task2_start_end:
            return False

    # handle comparison for daily/weekly tasks 
    else:
        # check for cases where the daily task only exists for a short period in between two instances of the weekly task, return False
        if task1.frequency == 1 and task2.frequency == 7:
            if task1_start > task2_start_end and task1_end_date_end < task2_end_date:
                return False
        else:
            if task2_start > task1_start_end and task2_end_date_end < task1_end_date:
                return False
            
        # assume matching dates to make accounting for tasks that span multiple days easier
        task1_start_modified = modify_date(task1_start, task2_start)
        task1_start_end_modified = get_datetime_from_dur(task1_start_modified, task1.duration)
        # if times never overlap, return False
        if task1_start_end_modified <= task2_start or task1_start_modified >= task2_start_end:
            return False
        
    # default to return True
    return True


# compare one transient and one recurring task
def diff_tasks_overlap(rectask: RecurringTask, tratask: TransientTask):

    # start datetime & end datetime for the first instance of the recurring task
    rec_start = get_datetime_from_datetime(rectask.start_date, rectask.start_time)
    rec_start_end = get_datetime_from_dur(rec_start, rectask.duration)
    rec_weekday = rec_start.weekday

    # start datetime & end datetime for the last instance of the recurring task
    if rectask.frequency == 1:
        rec_end_date = get_datetime_from_datetime(rectask.end_date, rectask.start_time)
        rec_end_date_end = get_datetime_from_dur(rec_end_date, rectask.duration)
    elif rectask.frequency == 7:
        rec_end_date = get_datetime_from_datetime(rectask.end_date, rectask.start_time)
        
        # decrement end_date datetime by a day until it's the correct weekday
        while (rec_end_date.weekday != rec_weekday):
            rec_end_date -= timedelta(days=1)
        rec_end_date_end = get_datetime_from_dur(rec_end_date, rectask.duration)
    
    # start and end datetimes for transient task
    tra_start = get_datetime_from_datetime(tratask.start_date, tratask.start_time)
    tra_end = get_datetime_from_dur(tra_start, tratask.duration)

    return True


# output new datetime with time of datetime1 and date of datetime2
def modify_date(datetime1: datetime, datetime2: datetime):
    # Extract the time part from datetime1
    time_part = datetime1.time()
    
    # Extract the date part from datetime2
    date_part = datetime2.date()
    
    # Combine date part from datetime2 and time part from datetime1
    new_datetime = datetime.combine(date_part, time_part)
    
    return new_datetime


# output new datetime with the time and weekday of datetime1 and the date of datetime2
def modify_week(datetime1, datetime2):
    # Extract the time part from datetime1
    time_part = datetime1.time()
    
    # Extract the date part from datetime2
    date_part = datetime2.date()

    weekday_dif = datetime1.weekday - datetime2.weekday
    
    # Combine date part from datetime2 and time part from datetime1
    new_datetime = datetime.combine(date_part, time_part)
    new_datetime += timedelta(days=weekday_dif)
    
    return new_datetime



# verifies that an anti-task can be applied to an instance of a recurring task
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
def get_datetime_from_date(date: int):
    date_str = str(date)   # YYYYMMDD
    year = int(date_str[0:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return datetime(year, month, day)

# returns datetime object with time
def get_datetime_from_datetime(date: int, time: float):
    hours = int(time)
    minute_dict = {0.00: 0, 0.25: 15, 0.50: 30, 0.75: 45}
    minutes = minute_dict[time - hours]
    date_str = str(date)   # YYYYMMDD
    year = int(date_str[0:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return datetime(year, month, day, hour=hours, minute=minutes)

# adds specified duration to existing datetime, returns new datetime
def get_datetime_from_dur(start: datetime, dur: float):

    #convert duration to timedelta object
    hour_delta = int(dur)
    minute_dict = {0.00: 0, 0.25: 15, 0.50: 30, 0.75: 45}
    minute_delta = minute_dict[dur - hour_delta]
    time_dur = timedelta(hours=hour_delta, minutes=minute_delta)

    # add timedelta to existing datetime
    return start + time_dur


# returns weekday from integer date
def get_day_of_week(date):
    date_obj = get_datetime_from_date(date)
    return date_obj.weekday()


class Model:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        #A ttempts to create the task. Returns True if it fits the schedule, or False otherwise
        for existing_task in self.tasks:
            if check_overlap(existing_task, task):
                raise ValueError('New task overlaps with an existing task')

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
    
