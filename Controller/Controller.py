from Model import Model

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

    pass