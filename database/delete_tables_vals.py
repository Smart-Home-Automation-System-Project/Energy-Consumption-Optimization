import sqlite3
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def delete_from_devices():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM devices")
        conn.commit()
        print("✅ Cleared values from 'devices' table.")

def delete_from_real_time_energy_readings():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM real_time_energy_readings")
        conn.commit()
        print("✅ Cleared values from 'real_time_energy_readings' table.")

def delete_from_historical_energy_readings():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM historical_energy_readings")
        conn.commit()
        print("✅ Cleared values from 'historical_energy_readings' table.")

def delete_from_predictions():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM predictions")
        conn.commit()
        print("✅ Cleared values from 'predictions' table.")

def delete_from_scheduled_tasks():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM scheduled_tasks")
        conn.commit()
        print("✅ Cleared values from 'scheduled_tasks' table.")

def delete_from_anomalies():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM anomalies")
        conn.commit()
        print("✅ Cleared values from 'anomalies' table.")

def delete_all_values():
    delete_from_devices()
    delete_from_real_time_energy_readings()
    delete_from_historical_energy_readings()
    delete_from_predictions()
    delete_from_scheduled_tasks()

# delete_all_values()
# delete_from_historical_energy_readings()
# delete_from_predictions()
delete_from_scheduled_tasks()
# delete_from_real_time_energy_readings()
# delete_from_devices()
# delete_from_anomalies()
