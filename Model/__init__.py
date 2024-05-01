from ..Task import Task, RecurringTask, TransientTask, AntiTask

recurring_tasks = []
transient_tasks = []
anti_tasks = []

class Model:
    #def create_recurring_task(name: str, start_time: float, duration: float, start_date: int, type: str) -> bool:
    def add_recurring_task(task: RecurringTask):
        """Attempts to create the recurring task. Returns True if its valid, or False otherwise"""

        pass

    def is_task_valid():
