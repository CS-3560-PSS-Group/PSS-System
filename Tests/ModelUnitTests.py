import unittest
import operator
from Model.Model import Model
from Task.Task import Task, RecurringTask, TransientTask, AntiTask


class TestModel(unittest.TestCase):

    def test_add_two_valid(self):
        test_model = Model()
        test_task1 = TransientTask("test", "test", 20240515, 12.00, 1.00)
        test_task2 = TransientTask("test", "test", 20240515, 13.00, 1.00)
        test_model.add_task(test_task1)
        result = test_model.add_task(test_task2)
        self.assertEqual(result, True, 'Adding two adjacent transient tasks to model failed.')
    
    def test_add_two_invalid(self):
        test_model = Model()
        test_task1 = TransientTask("test", "test", 20240515, 12.00, 1.00)
        test_task2 = TransientTask("test", "test", 20240515, 12.00, 1.00)
        test_model.add_task(test_task1)
        self.assertRaises(ValueError, lambda: test_model.add_task(test_task2))

    def test_add_three_partially_valid(self):
        test_model = Model()
        test_task1 = TransientTask("test", "test", 20240515, 12.00, 1.00)
        test_task2 = TransientTask("test", "test", 20240515, 12.50, 1.00)
        test_model.add_task(test_task1)
        self.assertRaises(ValueError, lambda: test_model.add_task(test_task2))

if __name__ == '__main__':
    unittest.main()