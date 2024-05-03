from datetime import datetime, timedelta


class Task:
    def __init__(self, name: str, task_type: str, start_date: int, start_time: float, duration: float):
        self.name = name
        self.task_type = task_type
        self.start_time = start_time
        self.duration = duration
        self.start_date = start_date

        # Validate values
        if self.start_time < 0 or self.start_time > 23.75:
            raise ValueError("Start time must be between 0 and 23.75")

        if self.duration < 0.25 or self.duration > 23.75:
            raise ValueError("Duration must be between 0.25 and 23.75")


# it is assumed that a recurring task will have it's end_date set at or after the last week day. In other words, end_date can't be 5/1/24 when Thursday is set to True.
class RecurringTask(Task):
    def __init__(self, name: str, task_type: str, start_date: int, start_time: float, duration: float, end_date: int, frequency: int): 
        super().__init__(name, task_type, start_date, start_time, duration)
        self.end_date = end_date
        self.frequency = frequency
        self.anti_tasks = []
    def add_anti_task(self, anti_task):
        self.anti_tasks.append(anti_task)
        # check to see if end_date is after last week day ... ?


def get_datetime_from_date(date):
    date_str = str(date)   # YYYYMMDD
    year = int(date_str[0:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return datetime(year, month, day)

def get_date_from_datetime(date_obj):
    return int(date_obj.strftime('%Y%m%d'))
 
# just checks to see if recurring tasks occur on the same day, but does NOT check if they occur at the same TIME of day.
def do_recurring_tasks_share_common_day( task1: RecurringTask, task2: RecurringTask):
    num_daily = 0 # how many tasks occur daily. if both are daily, then 2. if only one is daily, and other is weekly, then num_daily = 1
    if task1.frequency == 1:
        num_daily+=1
    if task2.frequency == 1:
        num_daily+=1

    start_date_obj_1 = get_datetime_from_date(task1.start_date)
    start_date_obj_2 = get_datetime_from_date(task2.start_date)

    if num_daily == 0:  # weekly and weekly
        
        days_difference = abs((start_date_obj_2 - start_date_obj_1).days)

        if days_difference % 7 == 0:  # if these two occur on the same weekday
            latest_start_date = max(task1.start_date, task2.start_date)
            earliest_end_date = min(task1.end_date, task2.end_date)
            return latest_start_date <= earliest_end_date
        else:
            return False

    elif num_daily == 1:
        if task1.frequency != 1:  # I want task1 to be the one thats daily. if its task2, then swap them.
            task1, task2 = task2, task1
            start_date_obj_1, start_date_obj_2 = start_date_obj_2, start_date_obj_1
        
        if task1.start_date > task2.start_date: # if the daily task starts after the weekly one, then latest_start_date will be the first occurrence of the weekly task that comes after daily tasks's start
            days_offset = (start_date_obj_2 - start_date_obj_1).days % 7

            days_to_add = 0 if days_offset == 0 else 7 - days_offset
            latest_start_date_obj = start_date_obj_1 + timedelta(days=days_to_add)  
            latest_start_date = get_date_from_datetime(latest_start_date_obj)
        else:
            latest_start_date = task2.start_date
        
        earliest_end_date = min(task1.end_date, task2.end_date)
        return latest_start_date <= earliest_end_date

    elif num_daily == 2:
        latest_start_date = max(task1.start_date, task2.start_date)
        earliest_end_date = min(task1.end_date, task2.end_date)
        return latest_start_date <= earliest_end_date

def do_recurring_tasks_collide( task1: RecurringTask, task2: RecurringTask):
    pass

t1 = RecurringTask("Task one", "...", 20240510, 0, 0.25, 20240510, 1)
t2 = RecurringTask("Task two", "...", 20240509, 0, 0.25, 202405028, 1)

print(do_recurring_tasks_collide(t1, t2))