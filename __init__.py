from Model import Model
from Task import Task, RecurringTask, TransientTask, AntiTask

t1 = RecurringTask("Task one", "...", 20200501, 9, 1.5, 20240510, 1)
t2 = RecurringTask("Task two", "...", 20240509, 0, 0.25, 202405028, 1)

model = Model()

model.add_task(t1)
model.add_task(t2)

model.import_schedule_from_json('''
[
  {
    "Name" : "Dinner",
    "Type" : "Meal",
    "StartDate" : 20200414,
    "StartTime" : 17,
    "Duration" : 1,
    "EndDate" : 20200507,
    "Frequency" : 1
  },
  {
    "Name" : "Homework",
    "Type" : "Study",
    "StartDate" : 20200414,
    "StartTime" : 15,
    "Duration" : 1,
    "EndDate" : 20200507,
    "Frequency" : 1
  },
  {
    "Name" : "Going to Mall",
    "Type" : "Shopping",
    "Date" : 20200501,
    "StartTime" : 10,
    "Duration" : 1.5
  }
]''')

print(model.dump_full_schedule_to_json())