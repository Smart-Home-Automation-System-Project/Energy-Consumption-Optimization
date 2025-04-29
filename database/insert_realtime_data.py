# insert_realtime_data.py
import sqlite3
import random
from datetime import datetime, timedelta
import export_realtime_to_csv

conn = sqlite3.connect("database2.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM devices")
devices = cursor.fetchall()

if len(devices) == 0:
    raise ValueError("No devices found in the 'devices' table.")

start_date = datetime.now() - timedelta(hours=10)
end_date = datetime.now()
interval = timedelta(minutes=1)

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


def anomaly_value(device_type):
    # Slightly randomized upper limits for each device
    anomaly_ranges = {
        "AC": (300, 700),
        "Microwave": (1300, 1600),
        "Refrigerator": (100, 200),
        "Dishwasher": (1400, 1800),
        "Smart Plug": (250, 400),
        "Washing Machine": (300, 1500),
        "TV": (70, 150),
        "Light": (120, 200)
    }
    default_range = (400, 600)
    return round(random.uniform(*anomaly_ranges.get(device_type, default_range)), 2)


# Inject 1% anomalies
anomaly_count = int(0.01 * len(timestamps) * len(devices))
anomaly_indices = set(random.sample(range(len(timestamps) * len(devices)), anomaly_count))

print(f"Injecting {anomaly_count} anomalies...")

index = 0
for ts in timestamps:
    sample_size = min(len(devices), random.randint(5, min(12, len(devices))))
    active_devices = random.sample(devices, sample_size)
    for device in active_devices:
        if index in anomaly_indices:
            watts = anomaly_value(device[3])
        else:
            watts = round(realistic_power(device[3]), 2)

        cursor.execute("""
            INSERT OR IGNORE INTO real_time_energy_readings (switch_id, timestamp, power_consumption)
            VALUES (?, ?, ?)
        """, (device[0], ts.strftime("%Y-%m-%d %H:%M:%S"), watts))

        index += 1

conn.commit()
conn.close()
export_realtime_to_csv.export_realtime_data()
print(f"✅ Realtime data inserted for {len(timestamps)} minutes ({start_date} to {end_date})")
