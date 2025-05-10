import os
import sqlite3
import unittest
from datetime import datetime, timedelta
import importlib.util

class TestInsertRealtimeData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Path to the database
        cls.db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'database.db')
        cls.db_path = os.path.abspath(cls.db_path)

        # Ensure the 'devices' table is created and populated
        cls.create_devices_table()

        # Run the script once
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'insert_realtime_data.py')
        spec = importlib.util.spec_from_file_location("insert_realtime_data", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    @classmethod
    def create_devices_table(cls):
        # Create a new database connection and cursor
        conn = sqlite3.connect(cls.db_path)
        cursor = conn.cursor()

        # Create the 'devices' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                device_type TEXT NOT NULL,
                wattage_range TEXT NOT NULL
            )
        """)

        # Insert mock device data if the table is empty
        cursor.execute("SELECT COUNT(*) FROM devices")
        count = cursor.fetchone()[0]
        if count == 0:
            # Insert some sample devices
            cursor.executemany("""
                INSERT INTO devices (name, device_type, wattage_range) 
                VALUES (?, ?, ?)
            """, [
                ('Device 1', 'AC', '300-700'),
                ('Device 2', 'Microwave', '900-1200'),
                ('Device 3', 'Refrigerator', '100-200')
            ])

        conn.commit()
        conn.close()

    def test_devices_table_not_empty(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM devices")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(count, 0, "Devices table should not be empty")

    def test_realtime_data_inserted(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check readings inserted in the last ~11 hours
        time_threshold = (datetime.now() - timedelta(hours=11)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            SELECT COUNT(*) FROM real_time_energy_readings
            WHERE timestamp > ?
        """, (time_threshold,))
        count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(count, 0, "Real-time energy readings should have been inserted")

if __name__ == '__main__':
    unittest.main()
