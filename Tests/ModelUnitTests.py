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

    def test_full_transient_overlap(self):
        test_model = Model()
        test_task1 = TransientTask("test", "test", 20240515, 23.50, 1.00)
        test_task2 = TransientTask("test", "test", 20240515, 23.00, 2.00)
        test_model.add_task(test_task1)
        self.assertRaises(ValueError, lambda: test_model.add_task(test_task2))

    def test_two_valid_recurring_daily(self):
        test_model = Model()
        test_task1 = RecurringTask("test", "test", 20240515, 20.00, 1.00, 20240615, 1)
        test_task2 = RecurringTask("test", "test", 20240515, 18.00, 1.00, 20240615, 1)
        test_model.add_task(test_task1)
        result = test_model.add_task(test_task2)
        self.assertEqual(result, True, 'Adding daily recurring tasks to model failed.')

    def test_two_invalid_recurring_daily(self):
        test_model = Model()
        test_task1 = RecurringTask("test", "test", 20240515, 20.00, 1.00, 20240615, 1)
        test_task2 = RecurringTask("test", "test", 20240515, 19.50, 1.00, 20240615, 1)
        test_model.add_task(test_task1)
        self.assertRaises(ValueError, lambda: test_model.add_task(test_task2))

    def test_two_valid_recurring_weekly(self):
        test_model = Model()
        test_task1 = RecurringTask("test", "test", 20240515, 20.00, 1.00, 20240615, 7)
        test_task2 = RecurringTask("test", "test", 20240515, 18.00, 1.00, 20240615, 7)
        test_model.add_task(test_task1)
        result = test_model.add_task(test_task2)
        self.assertEqual(result, True, 'Adding daily recurring tasks to model failed.')

    def test_two_invalid_recurring_weekly(self):
        test_model = Model()
        test_task1 = RecurringTask("test", "test", 20240515, 20.00, 1.00, 20240615, 7)
        test_task2 = RecurringTask("test", "test", 20240515, 19.50, 1.00, 20240615, 7)
        test_model.add_task(test_task1)
        self.assertRaises(ValueError, lambda: test_model.add_task(test_task2))

    def test_weekly_and_daily_valid(self):
        test_model = Model()
        test_task1 = RecurringTask("test", "test", 20240515, 20.00, 1.00, 20240615, 7)
        test_task2 = RecurringTask("test", "test", 20240515, 18.00, 1.00, 20240615, 1)
        test_model.add_task(test_task1)
        result = test_model.add_task(test_task2)
        self.assertEqual(result, True, 'Adding daily and weekly recurring tasks to model failed.')

    def test_weekly_and_daily_invalid(self):
        test_model = Model()
        test_task1 = RecurringTask("test", "test", 20240515, 20.00, 1.00, 20240615, 7)
        test_task2 = RecurringTask("test", "test", 20240515, 19.50, 1.00, 20240615, 1)
        test_model.add_task(test_task1)
        self.assertRaises(ValueError, lambda: test_model.add_task(test_task2))

if __name__ == '__main__':
    unittest.main()