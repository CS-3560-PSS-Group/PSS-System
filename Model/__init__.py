from datetime import datetime, timedelta

from ..Task import Task, RecurringTask, TransientTask, AntiTask


def check_overlap(task1: Task, task2: Task):
    
    if type(task1) is TransientTask and type(task2) is TransientTask:
        return transient_datetimes_overlap(task1, task2)
    elif type(task1) is RecurringTask and type(task2) is RecurringTask:
        return recurring_tasks_overlap(task1, task2)

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
    
def recurring_tasks_overlap(task1: RecurringTask, task2: RecurringTask):

    # start datetime & end datetime for the first instance of the task
    task1_start = get_datetime_from_datetime(task1.start_date, task1.start_time)
    task1_start_end = get_datetime_from_dur(task1_start, task1.duration)
    task1_weekday = task1_start.weekday
    task1_end_weekday = task1_start_end.weekday

    # start datetime & end datetime for the last instance of the task
    if task1.frequency == 1:
        task1_end_date = get_datetime_from_datetime(task1.end_date, task1.start_time)
        task1_end_date_end = get_datetime_from_dur(task1_end_date, task1.duration)
    elif task1.frequency == 7:
        task1_end_date = get_datetime_from_datetime(task1.end_date, task1.start_time)
        
        # decrement end_date datetime by a day until it's the correct weekday
        while (task1_end_date.weekday > task1_weekday):
            task1_end_date -= timedelta(days=1)
        task1_end_date_end = get_datetime_from_dur(task1_end_date, task1.duration)

    # same structure as above but for task2
    task2_start = get_datetime_from_datetime(task2.start_date, task2.start_time)
    task2_start_end = get_datetime_from_dur(task2_start, task2.duration)
    task2_weekday = task2_start.weekday
    task2_end_weekday = task2_start_end.weekday

    if task2.frequency == 1:
        task2_end_date = get_datetime_from_datetime(task2.end_date, task2.start_time)
        task2_end_date_end = get_datetime_from_dur(task2_end_date, task2.duration)
    elif task2.frequency == 7:
        task2_end_date = get_datetime_from_datetime(task2.end_date, task2.start_time)
        while (task2_end_date.weekday > task2_weekday):
            task2_end_date -= timedelta(days=1)
        task2_end_date_end = get_datetime_from_dur(task2_end_date, task2.duration)

    # if their dates never overlap, return False
    if task1_end_date_end <= task2_start or task1_start >= task2_end_date_end:
        return False
    
    """    
    # THE FOLLOWING CODE IN THIS METHOD DOES NOT LOGICALLY WORK YET I AM TOO TIRED TO CONTINUE TODAY
    # if they both repeat weekly and their times never overlap, return false
    elif task1.frequency == 7 and task2.frequency == 7:
        # if their weekdays never overlap, return false
        if task1_end_weekday < task2_weekday or task1_weekday > task2_end_weekday:
            return False
        # if weekkdays do overlap but their times never do, 
        elif (task1_start_end.time <= task2_start.time and task1_end_weekday <= task2_weekday) or (task1_start.time >= task2_start_end.time and task1_weekday >= task2_end_weekday):
            return False

    # if either task repeats daily and their times never overlap, return false    
    else:
        if task1_start_end.time <= task2_start.time or task1_start.time >= task2_start_end.time:
            return False
    """



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
   
    """

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
    
