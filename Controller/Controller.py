from Model import Model

class Controller():
    def __init__(self):
        self.model = Model()
    
    def find_task_by_name(self, name: str):
        return self.model.find_task_by_name(name)
    
    pass