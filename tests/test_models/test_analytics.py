import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the models directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../models')))

# Import the module to test
from models import analytics

class TestAnalytics(unittest.TestCase):
    
    @patch('models.analytics.sqlite3.connect')
    def test_get_db_connection(self, mock_connect):
        """Test that get_db_connection establishes a connection properly"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        # Call the function
        conn = analytics.get_db_connection()
        
        # Verify the connection was established
        self.assertEqual(conn, mock_conn)
        self.assertTrue(mock_connect.called)
        print("✅ get_db_connection() establishes database connection correctly.")
    
    @patch('models.analytics.get_db_connection')
    def test_get_power_usage_stats(self, mock_get_db):
        """Test that get_power_usage_stats returns the expected structure"""
        # Create mock objects
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock the first query result (avg, min, max)
        mock_cursor.fetchone.side_effect = [
            (250.5, 50.2, 500.8),  # First fetchone call (avg, min, max)
            (12.5,)                # Second fetchone call (daily_kwh)
        ]
        
        # Mock the device contributions result
        mock_cursor.fetchall.return_value = [
            ('AC', 1500.5, 45.2),
            ('Light', 500.3, 15.1),
            ('Refrigerator', 800.1, 24.3)
        ]
        
        # Call the function
        result = analytics.get_power_usage_stats()
        
        # Verify it was called correctly
        self.assertTrue(mock_cursor.execute.called)
        
        # Check the result has the expected structure
        self.assertIn('average_power', result)
        self.assertIn('min_power', result)
        self.assertIn('max_power', result)
        self.assertIn('daily_kwh', result)
        self.assertIn('device_contributions', result)
        
        # Check that device_contributions has the expected length
        self.assertEqual(len(result['device_contributions']), 3)
        print("✅ get_power_usage_stats() returns data with correct structure and values.")
    
    @patch('models.analytics.get_db_connection')
    def test_get_hourly_usage_today(self, mock_get_db):
        """Test that get_hourly_usage_today returns the expected structure"""
        # Create mock objects
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock the query result
        mock_cursor.fetchall.return_value = [
            ('08', 200.5),
            ('09', 250.3),
            ('10', 300.1)
        ]
        
        # Call the function
        result = analytics.get_hourly_usage_today()
        
        # Verify it was called correctly
        self.assertTrue(mock_cursor.execute.called)
        
        # Check the result has the expected structure
        self.assertIn('hours', result)
        self.assertIn('values', result)
        
        # Check that hours and values have the expected length
        self.assertEqual(len(result['hours']), 3)
        self.assertEqual(len(result['values']), 3)
        print("✅ get_hourly_usage_today() returns correctly formatted hourly usage data.")

if __name__ == '__main__':
    unittest.main()