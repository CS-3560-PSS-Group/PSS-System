class Task:
    def __init__(self, name, task_type, start_time, duration, date):
        self.name = name
        self.task_type = task_type
        self.date = date
        self.start_time = round(start_time * 4) / 4  # rounding to the nearest 15 minutes
        self.duration = round(duration * 4) / 4  # rounding to the nearest 15 minutes
        self.end_time = self.start_time + self.duration
        self.check_restrictions()

    def check_restrictions(self):
        # Check start time restrictions
        if self.start_time < 0 or self.start_time > 23.75:
            raise ValueError("Start time must be between 0 and 23.75")

        # Check duration restrictions
        if self.duration < 0.25 or self.duration > 23.75:
            raise ValueError("Duration must be between 0.25 and 23.75")

        # Check uniqueness of task names (assuming tasks are unique within a date)
        if self.name in Task.task_names.get(self.date, []):
            raise ValueError("Task names must be unique")

        # Store task name for uniqueness check
        Task.task_names.setdefault(self.date, []).append(self.name)

    def overlaps_with(self, other_task):
        return not (self.end_time <= other_task.start_time or self.start_time >= other_task.end_time)

    def __str__(self):
        return f"Task: {self.name}, Type: {self.task_type}, Start Time: {self.start_time}, Duration: {self.duration}, Date: {self.date}"

# Class attribute to store task names by date for uniqueness check
Task.task_names = {}

# Example usage:
task1 = Task("Meeting", "Work", 8.25, 1.5, 20240425)
task2 = Task("Conference", "Work", 9.5, 1.25, 20240425)

# Checking for overlap
if task1.overlaps_with(task2):
    print("Tasks overlap")
else:
    print("Tasks do not overlap")

# Adding a task with the same name and date (which violates uniqueness)
try:
    task3 = Task("Meeting", "Work", 10.0, 2.0, 20240425)
except ValueError as e:
    print("Error:", e)


class RecurringTask(Task):
    def __init__(self, name, task_type, start_date, start_time, duration, end_date, frequency):
        super().__init__(name, task_type, start_time, duration, start_date)
        self.end_date = end_date
        self.frequency = frequency

    def __str__(self):
        return f"Recurring Task: {self.name}, Type: {self.task_type}, Start Date: {self.date}, Start Time: {self.start_time}, Duration: {self.duration}, End Date: {self.end_date}, Frequency: {self.frequency}"

# Example usage:
recurring_task1 = RecurringTask("Weekly Meeting", "Work", 20240425, 8.25, 1.5, 20240725, 7)
print(recurring_task1)

class TransientTask(Task):
    def __init__(self, name, task_type, date, start_time, duration):
        super().__init__(name, task_type, start_time, duration, date)

    def __str__(self):
        return f"Transient Task: {self.name}, Type: {self.task_type}, Date: {self.date}, Start Time: {self.start_time}, Duration: {self.duration}"

# Example usage:
transient_task1 = TransientTask("Doctor's Appointment", "Health", 20240425, 10.5, 1)
print(transient_task1)

class AntiTask:
    def __init__(self, name, task_type, date, start_time, duration):
        self.name = name
        self.task_type = task_type
        self.date = date
        self.start_time = start_time
        self.duration = duration

    def matches_recurring_task(self, recurring_task):
        """
        Checks if the anti-task matches the given recurring task.
        """
        return (
            self.date == recurring_task.date
            and self.start_time == recurring_task.start_time
            and self.duration == recurring_task.duration
        )

    def __str__(self):
        return f"Anti-Task: {self.name}, Type: {self.task_type}, Date: {self.date}, Start Time: {self.start_time}, Duration: {self.duration}"

# Example usage:
anti_task1 = AntiTask("Cancel Weekly Meeting", "Work", 20240425, 8.25, 1.5)
print(anti_task1)
