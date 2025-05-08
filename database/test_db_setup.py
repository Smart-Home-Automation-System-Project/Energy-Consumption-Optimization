import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
import sqlite3

# Add the parent directory to sys.path to import the module being tested
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db_setup

class TestDatabaseSetup(unittest.TestCase):
    
    @patch('sqlite3.connect')
    @patch('os.path.dirname')
    @patch('os.path.join')
    def test_database_connection(self, mock_join, mock_dirname, mock_connect):
        """Test that the database connection is created with the correct path"""
        # Setup mocks
        mock_dirname.return_value = '/mock/dir'
        mock_join.return_value = '/mock/dir/database.db'
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Import the module again to execute the code
        import importlib
        importlib.reload(db_setup)
        
        # Verify connection was made with correct path
        mock_dirname.assert_called_once()
        mock_join.assert_called_once_with('/mock/dir', 'database.db')
        mock_connect.assert_called_once_with('/mock/dir/database.db')
        
    @patch('sqlite3.connect')
    def test_table_creation(self, mock_connect):
        """Test that all the required tables are created"""
        # Setup mock connection and cursor
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Import the module to execute the code
        import importlib
        importlib.reload(db_setup)
        
        # Verify tables created
        expected_calls = [
            # Verify devices table creation
            call("""
CREATE TABLE IF NOT EXISTS devices (
    switch_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    device_type TEXT NOT NULL,
    max_power_rating REAL
)
"""),
            # Verify real_time_energy_readings table creation
            call("""
CREATE TABLE IF NOT EXISTS real_time_energy_readings (
    switch_id TEXT NOT NULL,
    timestamp TIMESTAMP(3),   -- Specify timestamp data type with precision (optional)
    power_consumption REAL NOT NULL,
    PRIMARY KEY (switch_id, timestamp),
    FOREIGN KEY (switch_id) REFERENCES devices(switch_id)
)
"""),
            # Verify historical_energy_readings table creation
            call("""
CREATE TABLE IF NOT EXISTS historical_energy_readings (
    switch_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    power_consumption REAL NOT NULL,
    PRIMARY KEY (switch_id, timestamp),
    FOREIGN KEY (switch_id) REFERENCES devices(switch_id)
)
"""),
            # Verify predictions table creation
            call("""
CREATE TABLE IF NOT EXISTS predictions (
    timestamp TEXT NOT NULL,
    power_consumption REAL NOT NULL,
    PRIMARY KEY (timestamp)
)
"""),
            # Verify scheduled_tasks table creation
            call("""
CREATE TABLE IF NOT EXISTS scheduled_tasks (
    task_id INTEGER PRIMARY KEY,
    switch_id INTEGER NOT NULL,
    target_date TEXT NOT NULL,
    scheduled_time TEXT,
    status TEXT CHECK(status IN ('not_scheduled', 'scheduled', 'completed')) DEFAULT 'not_scheduled'
)
"""),
            # Verify anomalies table creation
            call("""
CREATE TABLE IF NOT EXISTS anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    switch_id TEXT NOT NULL,
    device_name TEXT NOT NULL,
    location TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    power_consumption REAL NOT NULL,
    max_power_rating REAL NOT NULL,
    excess REAL NOT NULL,
    FOREIGN KEY (switch_id) REFERENCES devices(switch_id)
)
""")
        ]
        
        # Check that execute was called for each CREATE TABLE statement
        self.assertEqual(mock_cursor.execute.call_count, len(expected_calls))
        mock_cursor.execute.assert_has_calls(expected_calls, any_order=False)
        
        # Verify that commit and close were called
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('sqlite3.connect')
    def test_exception_handling(self, mock_connect):
        """Test that exceptions during database operations are properly handled"""
        # Setup mock to raise an exception
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = sqlite3.Error("Mock database error")
        mock_connect.return_value = mock_conn
        
        # Import module and handle the exception that might be raised
        with self.assertRaises(sqlite3.Error):
            import importlib
            importlib.reload(db_setup)
            
        # Verify connect was called but commit and close weren't due to the exception
        mock_connect.assert_called_once()


if __name__ == '__main__':
    unittest.main()