import unittest
from Model.Model import Model
from Task.Task import Task, RecurringTask, TransientTask, AntiTask


class TestModel(unittest.TestCase):

    def test_add(self):
        test_model = Model()
        test_task = TransientTask("test", "test", 20240515, 12.00, 1.00)
        result = test_model.add_task(test_task)
        self.assertEqual(result, True, 'Adding a transient task to model failed')

if __name__ == '__main__':
    unittest.main()