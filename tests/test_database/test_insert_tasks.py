import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import sqlite3
from datetime import datetime
import importlib.util

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestInsertTasks(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        # Path to the module
        self.module_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "database", "insert_tasks.py"
        )
        
        # Expected tasks to be inserted
        self.expected_tasks = [
            ("wm_01", "2025-04-27", None, "not_scheduled"),  # Washing Machine task
            ("dw_01", "2025-04-30", None, "not_scheduled"),   # Dishwasher task
        ]
    
    @patch('sqlite3.connect')
    def test_task_insertion(self, mock_connect):
        """Test that tasks are inserted correctly"""
        # Setup mock database connection and cursor
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Run the script
        spec = importlib.util.spec_from_file_location("insert_tasks", self.module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Verify database connection was established
        mock_connect.assert_called_once()
        mock_conn.cursor.assert_called_once()
        
        # Verify executemany was called with the correct SQL and data
        mock_cursor.executemany.assert_called_once()
        
        # Extract the SQL and tasks from the call
        call_args = mock_cursor.executemany.call_args[0]
        sql = call_args[0]
        tasks = call_args[1]
        
        # Verify SQL contains expected components
        self.assertIn("INSERT OR IGNORE INTO scheduled_tasks", sql)
        self.assertIn("switch_id", sql)
        self.assertIn("target_date", sql)
        self.assertIn("scheduled_time", sql)
        self.assertIn("status", sql)
        
        # Verify tasks match the expected data
        self.assertEqual(tasks, self.expected_tasks)
        
        # Verify commit and close were called
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    @patch('sqlite3.connect', side_effect=sqlite3.Error("Test DB Error"))
    def test_database_error_handling(self, mock_connect):
        """Test error handling for database operations"""
        # Run the script and expect sqlite3.Error
        with self.assertRaises(sqlite3.Error):
            spec = importlib.util.spec_from_file_location("insert_tasks_db_error", self.module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
    
    @patch('os.path.dirname')
    @patch('sqlite3.connect')
    def test_database_path_construction(self, mock_connect, mock_dirname):
        """Test that the database path is constructed correctly"""
        # Setup mock for os.path.dirname
        mock_dirname.return_value = "/mock/path"
        
        # Setup mock database connection and cursor
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        # Run the script
        spec = importlib.util.spec_from_file_location("insert_tasks_path", self.module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Verify connect was called with the correct path
        expected_path = os.path.join("/mock/path", "database.db")
        mock_connect.assert_called_once_with(expected_path)
    
    def test_task_structure(self):
        """Test that the task data structure is correct"""
        for task in self.expected_tasks:
            # Verify each task has 4 elements
            self.assertEqual(len(task), 4)
            
            # Verify switch_id format
            self.assertIsInstance(task[0], str)
            self.assertTrue(task[0].startswith("wm_") or task[0].startswith("dw_"))
            
            # Verify date format (YYYY-MM-DD)
            self.assertIsInstance(task[1], str)
            self.assertRegex(task[1], r'^\d{4}-\d{2}-\d{2}$')
            
            # Verify scheduled_time is None
            self.assertIsNone(task[2])
            
            # Verify status is valid
            self.assertIsInstance(task[3], str)
            self.assertEqual(task[3], "not_scheduled")

if __name__ == '__main__':
    unittest.main()