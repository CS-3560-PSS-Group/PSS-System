

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

    # Adds an anti-task to this Recurring Task's list of anti-tasks (not utilized yet)
    def add_anti_task(self, anti_task):
        self.anti_tasks.append(anti_task)
        # check to see if end_date is after last week day ... ?

class TransientTask(Task):
    pass

class AntiTask(Task):
    def __init__(self, name: str, task_type: str, start_date: int, start_time: float, duration: float): 
        super().__init__(name, task_type, start_date, start_time, duration)
        self.task_reference = None

    # Assigns this anti-task to a specific recurring task (not utilized yet)
    def reference_task(self, task: RecurringTask):
        self.task_reference = task


# Represents a single event that will be displayed on the calendar. Similar, but not the same as Task, because tasks may repeat (recurring tasks), or be negations like the anti taks
class Event():
    def __init__(self, name: str, is_recurring: bool, task_type: str, weekday: int, time: float, duration: float, extra_info: str):
        self.name = name
        self.is_recurring = is_recurring
        self.task_type = task_type
        self.weekday = weekday
        self.time = time
        self.duration = duration
        self.extra_info = extra_info
