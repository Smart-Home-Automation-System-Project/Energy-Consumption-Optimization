# insert_train_data.py
import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("database2.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM devices")
devices = cursor.fetchall()

if len(devices) == 0:
    raise ValueError("No devices found in the 'devices' table.")

end_date = datetime.now() - timedelta(hours=10)
start_date = end_date - timedelta(days=7)
interval = timedelta(minutes=30)

timestamps = []
current = start_date
while current <= end_date:
    timestamps.append(current)
    current += interval

def realistic_power(device_type):
    ranges = {
        "AC": (300, 700),
        "Microwave": (900, 1200),
        "Refrigerator": (100, 200),
        "Dishwasher": (800, 1300),
        "Smart Plug": (30, 200),
        "Washing Machine": (300, 1500),
        "TV": (70, 150),
        "Light": (10, 100)
    }
    return random.uniform(*ranges.get(device_type, (50, 300)))


for ts in timestamps:
    sample_size = min(len(devices), random.randint(5, min(12, len(devices))))
    active_devices = random.sample(devices, sample_size)
    for device in active_devices:
        watts = round(realistic_power(device[3]), 2)
        cursor.execute("""
            INSERT OR IGNORE INTO historical_energy_readings (switch_id, timestamp, power_consumption)
            VALUES (?, ?, ?)
        """, (device[0], ts.strftime("%Y-%m-%d %H:%M:%S"), watts))

conn.commit()
conn.close()
print(f"✅ Historical data inserted from {start_date} to {end_date}")
