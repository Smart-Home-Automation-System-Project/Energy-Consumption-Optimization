import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import datetime, timedelta

# Devices
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

# Time setup
end_time = datetime.now()
start_time = end_time - timedelta(days=21)  # Last 21 days from today
timestamps = pd.date_range(start=start_time, end=end_time, freq='30min')[:-1]

# Track if kitchen AC has activated
kitchen_ac_start_times = {}
# Force kitchen AC to be active on first day
first_day = start_time.date()
kitchen_ac_start_times[first_day] = True

# Simulate usage
def simulate_usage(switch_id, device_type, max_power, hour, location, timestamp):
    rand = np.random.rand()
    is_bedroom = location.startswith("Bedroom")
    is_sleep_hour = (hour >= 23 or hour <= 6)
    is_weekend = timestamp.weekday() >= 5

    # Garden Light Logic
    if device_type == "Light" and location == "Garden":
        if 18 <= hour <= 23:
            return max_power * np.random.uniform(0.8, 1.0) * (1.3 if is_weekend else 1.0)
        return 0

    # Kitchen AC Logic (ac_03)
    if switch_id == "ac_03":
        day = timestamp.date()
        if day not in kitchen_ac_start_times:
            if 3 <= hour < 5 and rand > 0.5:
                kitchen_ac_start_times[day] = True
        if kitchen_ac_start_times.get(day, False):
            return max_power * np.random.uniform(0.7, 1.0) if is_weekend else max_power * np.random.uniform(0.4, 0.8)
        return 0

    # Living Room AC Logic
    if device_type == "AC" and location == "Living_Room":
        if hour >= np.random.choice([5,6,7,8]):
            if 20 <= hour <= 23:
                return max_power * np.random.uniform(0.8, 1.0) if is_weekend else max_power * np.random.uniform(0.6, 0.9)
            return max_power * np.random.uniform(0.5, 0.8) if is_weekend else max_power * np.random.uniform(0.3, 0.5)
        return 0

    # Bedroom Sleeping Logic
    if is_bedroom and is_sleep_hour:
        if device_type == "AC":
            return max_power * np.random.uniform(0.3, 0.5) if rand > 0.3 else 0
        elif device_type == "Light" or device_type == "Smart_Plug":
            return 0

    # Normal Logic with weekend/weekday variation
    if device_type == "AC":
        if 12 <= hour <= 16 or 20 <= hour <= 23:
            if is_weekend:
                return max_power * np.random.uniform(0.7, 1.0) if rand > 0.2 else 0
            return max_power * np.random.uniform(0.3, 0.7) if rand > 0.4 else 0
        return max_power * np.random.uniform(0.1, 0.3) if rand > 0.7 else 0
    elif device_type == "Microwave":
        if is_weekend:
            return max_power * np.random.uniform(0.6, 1.0) if hour in [7,8,12,13,18,19] and rand > 0.5 else 0
        return max_power * np.random.uniform(0.4, 0.8) if hour in [7,12,18] and rand > 0.7 else 0
    elif device_type == "Refrigerator":
        return max_power * np.random.uniform(0.2, 0.4)
    elif device_type == "Dishwasher":
        if is_weekend:
            return max_power * np.random.uniform(0.7, 1.0) if hour in [14,15,20,21,22] and rand > 0.2 else 0
        return max_power * np.random.uniform(0.4, 0.8) if hour in [20,21,22,23] and rand > 0.4 else 0
    elif device_type == "Washing_Machine":
        if is_weekend:
            return max_power * np.random.uniform(0.7, 1.0) if hour in [9,10,14,15] and rand > 0.3 else 0
        return max_power * np.random.uniform(0.4, 0.8) if hour in [9,14] and rand > 0.5 else 0
    elif device_type == "TV":
        if is_weekend:
            return max_power * np.random.uniform(0.5, 1.0) if (12 <= hour <= 23) and rand > 0.2 else 0
        return max_power * np.random.uniform(0.3, 0.7) if 18 <= hour <= 23 and rand > 0.4 else 0
    elif device_type == "Light":
        if is_weekend:
            return max_power * np.random.uniform(0.5, 1.0) if (18 <= hour <= 23 or hour <= 6) else 0
        return max_power * np.random.uniform(0.2, 0.8) if (18 <= hour <= 23 or hour <= 6) else 0
    elif device_type == "Smart_Plug":
        if is_weekend:
            return max_power * np.random.uniform(0.4, 1.0) if rand > 0.6 else 0
        return max_power * np.random.uniform(0.2, 0.7) if rand > 0.8 else 0
    return 0

# Generate data
records = []
for timestamp in timestamps:
    hour = timestamp.hour
    for device in devices:
        switch_id, _, location, device_type, max_power = device
        power = simulate_usage(switch_id, device_type, max_power, hour, location, timestamp)
        records.append((switch_id, timestamp.strftime("%Y-%m-%d %H:%M:%S"), round(power, 2)))

# Save to CSV
df = pd.DataFrame(records, columns=["switch_id", "timestamp", "power_consumption"])
df.to_csv("power_consumption_final.csv", index=False)

# Save to database
db_path = os.path.join(os.path.dirname(__file__), "database.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.executemany("""
    INSERT INTO historical_energy_readings (switch_id, timestamp, power_consumption)
    VALUES (?, ?, ?)
""", records)

conn.commit()
conn.close()

print("✅ Final data with weekday/weekend variation, sleeping, garden lights, kitchen & living AC rules saved and inserted into the database.")
