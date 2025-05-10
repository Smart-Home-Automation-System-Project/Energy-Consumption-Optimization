import unittest
import sqlite3
import os
import tempfile
from flask import Flask
from models.devices import get_devices, get_device_by_id
from models.database import init_app, get_db

class TestDevicesModel(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = Flask(__name__)
        self.app.config['DB_PATH'] = self.db_path
        self.app_context = self.app.app_context()
        self.app_context.push()
        init_app(self.app)

        db = get_db()
        db.execute('''
            CREATE TABLE devices (
                switch_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        db.execute('INSERT INTO devices (switch_id, name, status) VALUES (?, ?, ?)', (1, 'Device 1', 'on'))
        db.execute('INSERT INTO devices (switch_id, name, status) VALUES (?, ?, ?)', (2, 'Device 2', 'off'))
        db.commit()

    def tearDown(self):
        self.app_context.pop()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_get_devices_returns_all(self):
        devices = get_devices()
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]['name'], 'Device 1')
        self.assertEqual(devices[1]['status'], 'off')
        print("✅ get_devices() returns all devices correctly.")

    def test_get_device_by_id_valid(self):
        device = get_device_by_id(1)
        self.assertIsNotNone(device)
        self.assertEqual(device['name'], 'Device 1')
        print("✅ get_device_by_id() returns correct device for valid ID.")

    def test_get_device_by_id_invalid(self):
        device = get_device_by_id(999)
        self.assertIsNone(device)
        print("✅ get_device_by_id() returns None for invalid ID.")

    def test_get_device_by_id_edge_case(self):
        # Insert a device with ID 0 to test edge case
        db = get_db()
        db.execute('INSERT INTO devices (switch_id, name, status) VALUES (?, ?, ?)', (0, 'Edge Device', 'on'))
        db.commit()
        device = get_device_by_id(0)
        self.assertIsNotNone(device)
        self.assertEqual(device['name'], 'Edge Device')
        print("✅ get_device_by_id() handles edge case ID 0 correctly.")

if __name__ == '__main__':
    unittest.main()
