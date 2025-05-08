import unittest
from unittest.mock import patch, MagicMock, call
import sqlite3
import sys
import os

# Add the parent directory to sys.path to import the module being tested
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import delete_tables_vals

class TestDeleteTablesVals(unittest.TestCase):
    
    def setUp(self):
        # Save the original DB_PATH to restore it after tests
        self.original_db_path = delete_tables_vals.DB_PATH
    
    def tearDown(self):
        # Restore the original DB_PATH
        delete_tables_vals.DB_PATH = self.original_db_path
    
    @patch('sqlite3.connect')
    def test_delete_from_devices(self, mock_connect):
        """Test that DELETE FROM devices is executed correctly"""
        # Setup mock connection
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        # Call the function
        delete_tables_vals.delete_from_devices()
        
        # Verify connect was called with correct path
        mock_connect.assert_called_once_with(delete_tables_vals.DB_PATH)
        
        # Verify DELETE statement was executed
        mock_conn.execute.assert_called_once_with("DELETE FROM devices")
        
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    @patch('sqlite3.connect')
    def test_delete_from_real_time_energy_readings(self, mock_connect):
        """Test that DELETE FROM real_time_energy_readings is executed correctly"""
        # Setup mock connection
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        # Call the function
        delete_tables_vals.delete_from_real_time_energy_readings()
        
        # Verify connect was called with correct path
        mock_connect.assert_called_once_with(delete_tables_vals.DB_PATH)
        
        # Verify DELETE statement was executed
        mock_conn.execute.assert_called_once_with("DELETE FROM real_time_energy_readings")
        
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    @patch('sqlite3.connect')
    def test_delete_from_historical_energy_readings(self, mock_connect):
        """Test that DELETE FROM historical_energy_readings is executed correctly"""
        # Setup mock connection
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        # Call the function
        delete_tables_vals.delete_from_historical_energy_readings()
        
        # Verify connect was called with correct path
        mock_connect.assert_called_once_with(delete_tables_vals.DB_PATH)
        
        # Verify DELETE statement was executed
        mock_conn.execute.assert_called_once_with("DELETE FROM historical_energy_readings")
        
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    @patch('sqlite3.connect')
    def test_delete_from_predictions(self, mock_connect):
        """Test that DELETE FROM predictions is executed correctly"""
        # Setup mock connection
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        # Call the function
        delete_tables_vals.delete_from_predictions()
        
        # Verify connect was called with correct path
        mock_connect.assert_called_once_with(delete_tables_vals.DB_PATH)
        
        # Verify DELETE statement was executed
        mock_conn.execute.assert_called_once_with("DELETE FROM predictions")
        
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    @patch('sqlite3.connect')
    def test_delete_from_scheduled_tasks(self, mock_connect):
        """Test that DELETE FROM scheduled_tasks is executed correctly"""
        # Setup mock connection
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        # Call the function
        delete_tables_vals.delete_from_scheduled_tasks()
        
        # Verify connect was called with correct path
        mock_connect.assert_called_once_with(delete_tables_vals.DB_PATH)
        
        # Verify DELETE statement was executed
        mock_conn.execute.assert_called_once_with("DELETE FROM scheduled_tasks")
        
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    @patch('sqlite3.connect')
    def test_delete_from_anomalies(self, mock_connect):
        """Test that DELETE FROM anomalies is executed correctly"""
        # Setup mock connection
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        # Call the function
        delete_tables_vals.delete_from_anomalies()
        
        # Verify connect was called with correct path
        mock_connect.assert_called_once_with(delete_tables_vals.DB_PATH)
        
        # Verify DELETE statement was executed
        mock_conn.execute.assert_called_once_with("DELETE FROM anomalies")
        
        # Verify commit was called
        mock_conn.commit.assert_called_once()

    @patch('database.delete_tables_vals.delete_from_devices')
    @patch('database.delete_tables_vals.delete_from_real_time_energy_readings')
    @patch('database.delete_tables_vals.delete_from_historical_energy_readings')
    @patch('database.delete_tables_vals.delete_from_predictions')
    @patch('database.delete_tables_vals.delete_from_scheduled_tasks')
    def test_delete_all_values(self, mock_tasks, mock_predictions, 
                              mock_historical, mock_realtime, mock_devices):
        """Test that delete_all_values calls all individual delete functions"""
        # Call the function
        delete_tables_vals.delete_all_values()
        
        # Verify that each delete function was called once
        mock_devices.assert_called_once()
        mock_realtime.assert_called_once()
        mock_historical.assert_called_once()
        mock_predictions.assert_called_once()
        mock_tasks.assert_called_once()

    @patch('sqlite3.connect')
    def test_connection_error_handling(self, mock_connect):
        """Test that SQLite connection errors are properly handled"""
        # Setup mock to raise an exception when connecting
        mock_connect.side_effect = sqlite3.Error("Mock database connection error")
        
        # Call the function and expect the exception to be raised
        with self.assertRaises(sqlite3.Error):
            delete_tables_vals.delete_from_devices()

    @patch('sqlite3.connect')
    def test_execute_error_handling(self, mock_connect):
        """Test that SQLite execution errors are properly handled"""
        # Setup mock connection
        mock_conn = MagicMock()
        mock_conn.execute.side_effect = sqlite3.Error("Mock database execution error")
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        # Call the function and expect the exception to be raised
        with self.assertRaises(sqlite3.Error):
            delete_tables_vals.delete_from_devices()

    def test_custom_db_path(self):
        """Test that a custom DB_PATH can be set and is used correctly"""
        # Set a custom DB_PATH
        custom_path = "custom_database.db"
        delete_tables_vals.DB_PATH = custom_path
        
        with patch('sqlite3.connect') as mock_connect:
            # Setup mock connection
            mock_conn = MagicMock()
            mock_connect.return_value.__enter__.return_value = mock_conn
            
            # Call a function
            delete_tables_vals.delete_from_devices()
            
            # Verify connect was called with the custom path
            mock_connect.assert_called_once_with(custom_path)

if __name__ == '__main__':
    unittest.main()