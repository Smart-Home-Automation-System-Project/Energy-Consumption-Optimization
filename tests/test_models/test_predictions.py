import unittest
from unittest.mock import patch, MagicMock
import models.predictions as predictions_module


class TestPredictions(unittest.TestCase):

    @patch('models.predictions.get_db')
    def test_get_predictions(self, mock_get_db):
        mock_cursor = MagicMock()
        expected_data = [
            ('2025-05-10 08:00:00', 120.5),
            ('2025-05-10 09:00:00', 125.3)
        ]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        mock_get_db.return_value = mock_cursor

        result = predictions_module.get_predictions()
        self.assertEqual(result, expected_data)
        mock_cursor.execute.assert_called_once_with(
            'SELECT timestamp, power_consumption FROM predictions ORDER BY timestamp'
        )
        print("✅ get_predictions() returns ordered prediction data.")

    @patch('models.predictions.get_db')
    def test_get_todays_predictions(self, mock_get_db):
        mock_cursor = MagicMock()
        expected_data = [
            ('2025-05-10 10:00:00', 110.0),
            ('2025-05-10 11:00:00', 115.0)
        ]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        mock_get_db.return_value = mock_cursor

        result = predictions_module.get_todays_predictions()
        self.assertEqual(result, expected_data)
        mock_cursor.execute.assert_called_once_with(
            'SELECT timestamp, power_consumption FROM predictions WHERE DATE(timestamp) = DATE("now") ORDER BY timestamp'
        )
        print("✅ get_todays_predictions() returns today's data correctly.")

    @patch('models.predictions.get_db')
    def test_get_hourly_average(self, mock_get_db):
        mock_cursor = MagicMock()
        expected_data = [
            ('08', 110.0),
            ('09', 120.0)
        ]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        mock_get_db.return_value = mock_cursor

        result = predictions_module.get_hourly_average()
        self.assertEqual(result, expected_data)
        self.assertEqual(len(result), 2)
        mock_cursor.execute.assert_called_once()
        print("✅ get_hourly_average() returns correct hourly averages.")

    @patch('models.predictions.get_db')
    def test_get_seven_day_predictions(self, mock_get_db):
        mock_cursor = MagicMock()
        expected_data = [
            ('2025-05-10 08:00:00', 100.0),
            ('2025-05-17 08:00:00', 105.0)
        ]
        mock_cursor.execute.return_value.fetchall.return_value = expected_data
        mock_get_db.return_value = mock_cursor

        result = predictions_module.get_seven_day_predictions()
        self.assertEqual(result, expected_data)
        self.assertEqual(result[0][1], 100.0)
        self.assertEqual(result[1][1], 105.0)
        mock_cursor.execute.assert_called_once()
        print("✅ get_seven_day_predictions() returns data for the next 7 days.")


if __name__ == '__main__':
    unittest.main()
