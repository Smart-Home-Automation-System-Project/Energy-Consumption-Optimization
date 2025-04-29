import sqlite3

# Connect to the database
conn = sqlite3.connect("database2.db")
cursor = conn.cursor()

# Create 'devices' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS devices (
    switch_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    device_type TEXT NOT NULL,
    max_power_rating REAL
)
""")

# Create 'real_time_energy_readings' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS real_time_energy_readings (
    switch_id TEXT NOT NULL,
    timestamp TIMESTAMP(3),   -- Specify timestamp data type with precision (optional)
    power_consumption REAL NOT NULL,
    PRIMARY KEY (switch_id, timestamp),
    FOREIGN KEY (switch_id) REFERENCES devices(switch_id)
)
""")

# Create 'historical_energy_readings' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS historical_energy_readings (
    switch_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    power_consumption REAL NOT NULL,
    PRIMARY KEY (switch_id, timestamp),
    FOREIGN KEY (switch_id) REFERENCES devices(switch_id)
)
""")

# Create 'predictions' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    timestamp TEXT NOT NULL,
    power_consumption REAL NOT NULL,
    PRIMARY KEY (timestamp)
)
""")

# Create 'scheduled_tasks' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS scheduled_tasks (
    task_id INTEGER PRIMARY KEY,
    switch_id INTEGER NOT NULL,
    target_date TEXT NOT NULL,
    scheduled_time TEXT,
    status TEXT CHECK(status IN ('not_scheduled', 'scheduled', 'completed')) DEFAULT 'not_scheduled'
)
""")

# Create 'anomalies' table
cursor.execute("""
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



conn.commit()
conn.close()

print("✅ Tables created: devices, real_time_energy_readings, historical_energy_readings, predictions")
