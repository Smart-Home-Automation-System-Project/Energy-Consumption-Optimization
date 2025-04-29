# insert_devices.py
import sqlite3
import export_devices_to_csv

conn = sqlite3.connect("database2.db")
cursor = conn.cursor()

devices = [
    ("ac_01", "AC1", "Bedroom", "AC", 700),
    ("ac_02", "AC2", "Living Room", "AC", 700),
    ("ac_03", "AC3", "Kitchen", "AC", 700),
    ("mw_01", "Microwave", "Kitchen", "Microwave", 1200),
    ("rf_01", "Refrigerator", "Kitchen", "Refrigerator", 200),
    ("dw_01", "Dishwasher", "Kitchen", "Dishwasher", 1500),
    ("sp_01", "SmartPlug1", "Living Room", "Smart Plug", 400),
    ("wm_01", "WashingMachine", "Laundry Room", "Washing Machine", 1500),
    ("tv_01", "TV", "Living Room", "TV", 150),
    ("lt_01", "Light1", "Living Room", "Light", 100),
    ("lt_02", "Light2", "Kitchen", "Light", 100),
    ("lt_03", "Light3", "Bedroom", "Light", 100),
    ("lt_04", "Light4", "Bathroom", "Light", 100),
    ("lt_05", "Light5", "Office", "Light", 100),
    ("lt_06", "Light6", "Garage", "Light", 100),
]

cursor.executemany("""
INSERT OR IGNORE INTO devices (switch_id, name, location, device_type, max_power_rating)
VALUES (?, ?, ?, ?, ?)
""", devices)

conn.commit()
conn.close()
export_devices_to_csv.export_devices()
print("✅ Devices inserted successfully")
