

class Task:
    def __init__(self, name, task_type, start_date: int, start_time, duration):
        self.name = name
        self.task_type = task_type
        self.start_time = start_time
        self.duration = duration
        self.start_date = start_date

class RecurringTask(Task):
    def __init__(self, name, task_type, start_date: int, start_time, duration, end_date: int, week_days: list[bool]):
        super().__init__(name, task_type, start_date, start_time, duration)
        self.end_date = end_date
        self.week_days = week_days

'''from TaskClass import Task, RecurringTask, TransientTask, AntiTask

recurring_tasks = []
transient_tasks = []
anti_tasks = []

class Model:
    #def create_recurring_task(name: str, start_time: float, duration: float, start_date: int, type: str) -> bool:
    def add_recurring_task(task: RecurringTask):
        """Attempts to create the recurring task. Returns True if its valid, or False otherwise"""

        pass

    def is_task_valid():
'''
 