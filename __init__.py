from Model.Model import Model
from Task.Task import Task, RecurringTask, TransientTask, AntiTask

t1 = RecurringTask("Task one", "...", 20240510, 0, 0.25, 20240510, 1)
t2 = RecurringTask("Task two", "...", 20240509, 0, 0.25, 202405028, 1)

model = Model()

model.add_task(t1)
model.add_task(t2)

print(model.dump_full_schedule_to_json())