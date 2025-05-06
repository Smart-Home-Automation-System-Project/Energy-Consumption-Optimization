# insert_devices.py
import sqlite3
import os
import export_devices_to_csv

db_path = os.path.join(os.path.dirname(__file__), "database.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

devices = [
    ("ac_01", "AC1", "Bedroom_1", "AC", 700),
    ("ac_02", "AC1", "Bedroom_2", "AC", 700),
    ("ac_03", "AC2", "Kitchen", "AC", 700),
    ("ac_04", "AC3", "Living_Room", "AC", 700),
    ("mw_01", "Microwave", "Kitchen", "Microwave", 1200),
    ("rf_01", "Refrigerator", "Kitchen", "Refrigerator", 200),
    ("dw_01", "Dishwasher", "Kitchen", "Dishwasher", 1500),
    ("sp_01", "SmartPlug1", "Living_Room", "Smart_Plug", 400),
    ("sp_02", "SmartPlug2", "Living_Room", "Smart_Plug", 400),
    ("sp_03", "SmartPlug1", "Bedroom_2", "Smart_Plug", 400),
    ("sp_04", "SmartPlug1", "Bedroom_2", "Smart_Plug", 400),
    ("sp_05", "SmartPlug1", "Bedroom_1", "Smart_Plug", 400),
    ("sp_06", "SmartPlug1", "Bedroom_1", "Smart_Plug", 400),
    ("sp_07", "SmartPlug1", "Kitchen", "Smart_Plug", 400),
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
]

cursor.executemany("""
INSERT OR IGNORE INTO devices (switch_id, name, location, device_type, max_power_rating)
VALUES (?, ?, ?, ?, ?)
""", devices)

conn.commit()
conn.close()
# export_devices_to_csv.export_devices()
print("✅ Devices inserted successfully")
