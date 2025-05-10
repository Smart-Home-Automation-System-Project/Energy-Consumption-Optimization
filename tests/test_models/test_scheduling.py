import unittest
from unittest.mock import patch, MagicMock
import models.scheduling as scheduling_module


class TestScheduling(unittest.TestCase):

    @patch('models.scheduling.get_db')
    def test_get_scheduled_tasks(self, mock_get_db):
        mock_cursor = MagicMock()
        expected_data = [
            (1, 101, 'Washing Machine', '2025-05-11', '08:00:00', 'scheduled'),
            (2, 102, 'Dishwasher', '2025-05-11', '09:00:00', 'not_scheduled')
        ]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        mock_get_db.return_value = mock_cursor

        result = scheduling_module.get_scheduled_tasks()
        self.assertEqual(result, expected_data)
        mock_cursor.execute.assert_called_once()
        print("✅ get_scheduled_tasks() returns upcoming scheduled tasks correctly.")

    @patch('models.scheduling.get_db')
    def test_get_available_devices(self, mock_get_db):
        mock_cursor = MagicMock()
        expected_data = [
            (101, 'Washing Machine'),
            (102, 'Dishwasher')
        ]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        mock_get_db.return_value = mock_cursor

        result = scheduling_module.get_available_devices()
        self.assertEqual(result, expected_data)
        self.assertTrue(all(d[1] in ['Washing Machine', 'Dishwasher'] for d in result))
        mock_cursor.execute.assert_called_once()
        print("✅ get_available_devices() returns only washing machine and dishwasher.")

    @patch('models.scheduling.get_db')
    def test_schedule_task(self, mock_get_db):
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_cursor

        result = scheduling_module.schedule_task(101, '2025-05-12')
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once_with(
            '''
        INSERT INTO scheduled_tasks (switch_id, target_date, status)
        VALUES (?, ?, 'not_scheduled')
    ''', (101, '2025-05-12'))
        mock_cursor.commit.assert_called_once()
        print("✅ schedule_task() inserts new task and commits successfully.")

    @patch('models.scheduling.get_db')
    def test_schedule_task_invalid_data(self, mock_get_db):
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("DB error")
        mock_get_db.return_value = mock_cursor

        with self.assertRaises(Exception):
            scheduling_module.schedule_task(None, None)
        print("✅ schedule_task() correctly raises error on invalid input.")


if __name__ == '__main__':
    unittest.main()
