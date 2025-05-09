import unittest
from unittest.mock import patch, MagicMock, call
import sqlite3
import sys
import os

# Add the parent directory to sys.path to import the module for testing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import module but don't execute it yet
import database.insert_devices as insert_devices_module

class TestInsertDevices(unittest.TestCase):
    
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
        
        # Protect original code from executing during import
        original_connect = sqlite3.connect
        original_join = os.path.join
        original_dirname = os.path.dirname
        
        # Replace with mocks during test
        sqlite3.connect = mock_connect
        os.path.join = mock_join
        os.path.dirname = mock_dirname
        
        try:
            # Import the module to execute the code
            import importlib
            importlib.reload(insert_devices_module)
            
            # Verify connection was made with correct path
            mock_dirname.assert_called_once()
            mock_join.assert_called_once_with('/mock/dir', 'database.db')
            mock_connect.assert_called_once_with('/mock/dir/database.db')
        finally:
            # Restore original functions
            sqlite3.connect = original_connect
            os.path.join = original_join
            os.path.dirname = original_dirname
    
    @patch('sqlite3.connect')
    def test_devices_insertion(self, mock_connect):
        """Test that devices are correctly inserted into the database"""
        # Setup mock connection and cursor
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Protect original code from executing during import
        original_connect = sqlite3.connect
        
        # Replace with mock during test
        sqlite3.connect = mock_connect
        
        try:
            # Import the module to execute the code
            import importlib
            importlib.reload(insert_devices_module)
            
            # Verify executemany was called with correct SQL and data
            mock_cursor.executemany.assert_called_once()
            
            # Get arguments passed to executemany
            call_args = mock_cursor.executemany.call_args
            sql_query = call_args[0][0]
            devices_data = call_args[0][1]
            
            # Verify SQL query format
            expected_sql = """
INSERT OR IGNORE INTO devices (switch_id, name, location, device_type, max_power_rating)
VALUES (?, ?, ?, ?, ?)
"""
            self.assertEqual(sql_query.strip(), expected_sql.strip())
            
            # Verify devices data content
            expected_devices = [
                ("ac_01", "AC1", "Bedroom_1", "AC", 700),
                ("ac_02", "AC1", "Bedroom_2", "AC", 700),
                ("ac_03", "AC2", "Kitchen", "AC", 700),
                ("ac_04", "AC3", "Living_Room", "AC", 700),
                ("mw_01", "Microwave", "Kitchen", "Microwave", 1200),
                ("rf_01", "Refrigerator", "Kitchen", "Refrigerator", 200),
                ("dw_01", "Dishwasher", "Kitchen", "Dishwasher", 1500),
                ("sp_01", "SmartPlug1", "Living_Room", "Smart_Plug", 400),
                ("sp_02", "SmartPlug2", "Living_Room", "Smart_Plug", 400),
                ("sp_03", "SmartPlug3", "Bedroom_2", "Smart_Plug", 400),
                ("sp_04", "SmartPlug4", "Bedroom_2", "Smart_Plug", 400),
                ("sp_05", "SmartPlug5", "Bedroom_1", "Smart_Plug", 400),
                ("sp_06", "SmartPlug6", "Bedroom_1", "Smart_Plug", 400),
                ("sp_07", "SmartPlug7", "Kitchen", "Smart_Plug", 400),
                ("wm_01", "WashingMachine", "Living_Room", "Washing_Machine", 1500),
                ("tv_01", "TV", "Living_Room", "TV", 150),
                ("B_01", "Bulb1", "Bedroom_1", "Light", 100),
                ("B_02", "Bulb2", "Bedroom_2", "Light", 100),
                ("B_03", "Bulb3", "Kitchen", "Light", 100),
                ("B_04", "Bulb4", "Washroom", "Light", 100),
                ("B_05", "Bulb5", "Living_Room", "Light", 100),
                ("B_06", "Bulb6", "Living_Room", "Light", 100),
                ("B_07", "Bulb7", "Living_Room", "Light", 100),
                ("B_08", "Bulb8", "Garden", "Light", 100),
                ("B_09", "Bulb9", "Garden", "Light", 100),
                ("B_10", "Bulb10", "Garden", "Light", 100),
                ("SVC_01", "SmartVacuumCleaner", "Living_Room", "Smart_Vacuum_Cleaner", 350),
            ]
            
            self.assertEqual(devices_data, expected_devices)
            
            # Verify commit and close were called
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
        finally:
            # Restore original function
            sqlite3.connect = original_connect
    
    @patch('sqlite3.connect')
    def test_error_handling_during_connection(self, mock_connect):
        """Test error handling during database connection"""
        # Setup mock to raise exception
        mock_connect.side_effect = sqlite3.Error("Mock connection error")
        
        # Protect original code from executing during import
        original_connect = sqlite3.connect
        
        # Replace with mock during test
        sqlite3.connect = mock_connect
        
        try:
            # Import the module and expect exception
            with self.assertRaises(sqlite3.Error):
                import importlib
                importlib.reload(insert_devices_module)
        finally:
            # Restore original function
            sqlite3.connect = original_connect
    
    @patch('sqlite3.connect')
    def test_error_handling_during_execution(self, mock_connect):
        """Test error handling during SQL execution"""
        # Setup mocks
        mock_cursor = MagicMock()
        mock_cursor.executemany.side_effect = sqlite3.Error("Mock execution error")
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Protect original code from executing during import
        original_connect = sqlite3.connect
        
        # Replace with mock during test
        sqlite3.connect = mock_connect
        
        try:
            # Import the module and expect exception
            with self.assertRaises(sqlite3.Error):
                import importlib
                importlib.reload(insert_devices_module)
                
            # Verify connection was made but commit and close weren't called
            mock_connect.assert_called_once()
            mock_conn.commit.assert_not_called()
            # We can't verify close wasn't called because it might be in a finally block
        finally:
            # Restore original function
            sqlite3.connect = original_connect

if __name__ == '__main__':
    unittest.main()