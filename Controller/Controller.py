from Model import Model

from Task import Event

import json

def get_days_for_month(start_date):
    pass

class Controller():
    def __init__(self):
        self.model = Model()
    
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
            days = 30# johnathans_function(start_date)

        events = self.model.get_events_within_timeframe(start_date, days)

        json_str = json.dumps([event.to_dict() for event in events], indent=2)
        with open(file_name, 'w') as file:
            file.write(json_str)

            

    def get_events_within_timeframe(self, start_date: int, days: int) -> list[Event]:
        return self.model.get_events_within_timeframe(start_date, days)

    pass