from datetime import datetime

from ..Task import Event, Task, RecurringTask, TransientTask, AntiTask


def do_times_overlap(start_time1, duration1, start_time2, duration2):
    # two times overlap IF (StartA <= EndB) and (EndA >= StartB)...
    return start_time1 <= start_time2 + duration2 and start_time1 + duration1 >= start_time2

def do_dates_overlap(start_date1, end_date1, start_date2, end_date2):
    return start_date1 <= end_date2 and end_date1 >= start_date2

def get_datetime_from_date(date):
    date_str = str(date)   # YYYYMMDD
    year = int(date_str[0:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return datetime(year, month, day)

def get_day_of_week(date):
    date_obj = get_datetime_from_date(date)
    return date_obj.weekday()


class Model:
    def __init__(self):
        self.recurring_tasks: list[RecurringTask] = []
        self.transient_tasks: list[TransientTask] = []
        self.anti_tasks: list[AntiTask] = []

    def add_recurring_task(self, task: RecurringTask):
        """Attempts to create the recurring task. Returns True if it fits the schedule, or False otherwise"""
        for existing_task in self.recurring_tasks:
            if (any([task.week_days[i] and existing_task.week_days[i] for i in range(7)]) and   # check days of the week
                    do_dates_overlap(task.start_date, task.end_date, existing_task.start_date, existing_task.end_date) and    # check the actual start and end date
                    do_times_overlap(task.start_time, task.duration, existing_task.start_time, existing_task.duration)):      # check the time of the events during the day
                raise ValueError("New task overlaps with an existing task")
        
        for existing_task in self.transient_tasks:
            if self.do_recurring_and_transient_tasks_collide(task, existing_task):
                raise ValueError("New task overlaps with an existing task")

        self.recurring_tasks.append(task)

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
        
        return False # False if no recurring task collides with transient task


    def add_anti_task(self, task: AntiTask): 
        self.anti_tasks.append(task)

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


    '''def get_recurring_tasks():
        pass
    
    def get_transient_tasks(): 
        pass

    def get_anti_tasks():
        pass

    def is_task_valid():
        pass'''
    
