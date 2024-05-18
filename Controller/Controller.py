from Model import Model

from Task import Task, Event

import json

def get_days_for_month(start_date):
    pass

class Controller():
    def __init__(self):
        self.model = Model()
    
    # Add any kind of task. Can be Recurring, Transient, or Anti
    def add_task(self, task: Task):
        self.model.add_task(task)

    def find_task_by_name(self, name: str):
        return self.model.find_task_by_name(name)
    
    def export_schedule_to_json_file(self, file_name):
        schedule_json = self.model.dump_full_schedule_to_json()
        with open(file_name, 'w') as file:
            file.write(schedule_json)
        
    def import_schedule_from_json_file(self, file_name):
        with open(file_name, 'r') as file:
            contents = file.read()
            self.model.import_schedule_from_json(contents)        

    def write_schedule(self, file_name, start_date, schedule_type):
        if schedule_type == 'Day':
            days = 1    
        elif schedule_type == 'Week':
            days = 7
        else:
            days = 30

        events = self.model.get_events_within_timeframe(start_date, days)

        json_str = json.dumps([event.to_dict() for event in events], indent=2)
        with open(file_name, 'w') as file:
            file.write(json_str)

    def edit_task(self, task_name: str, task: Task):
        self.model.edit_task(task_name, task)

    def delete_task(self, task_name: str):
        self.model.delete_task(task_name)

    def get_events_within_timeframe(self, start_date: int, days: int) -> list[Event]:
        return self.model.get_events_within_timeframe(start_date, days)

    pass