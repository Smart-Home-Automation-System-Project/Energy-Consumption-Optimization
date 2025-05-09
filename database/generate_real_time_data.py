import sqlite3
import random
from datetime import datetime, timedelta
import time
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'database.db')

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print(f"Connected to database at: {db_path}")

# Retrieve all devices with full information for anomaly recording
cursor.execute("SELECT switch_id, name, location, device_type, max_power_rating FROM devices")
devices = cursor.fetchall()

# Create a dictionary for easy device lookup
device_dict = {device[0]: {"name": device[1], "location": device[2], "type": device[3], "max_power": device[4]} for device in devices}

# Define anomaly probability (5% chance)
p_anomaly = 0.05

# Define parameters for each device type
device_params = {
    'Light': {'p_on': 0.7, 'normal_range': [0.8, 1.0], 'anomaly_low': 0.5, 'anomaly_high': 1.1},
    'AC': {'p_on': 0.5, 'normal_range': [0.5, 1.0], 'anomaly_low': 0.2, 'anomaly_high': 1.1},
    'Microwave': {'p_on': 0.2, 'normal_range': [0.7, 1.0], 'anomaly_low': 0.3, 'anomaly_high': 1.1},
    'Dishwasher': {'p_on': 0.2, 'normal_range': [0.7, 1.0], 'anomaly_low': 0.3, 'anomaly_high': 1.1},
    'Washing_Machine': {'p_on': 0.2, 'normal_range': [0.7, 1.0], 'anomaly_low': 0.3, 'anomaly_high': 1.1},
    'Smart_Plug': {'p_on': 0.5, 'normal_range': [0.0, 1.0], 'anomaly_low': 0.0, 'anomaly_high': 1.1},
    'TV': {'p_on': 0.4, 'normal_range': [0.5, 1.0], 'anomaly_low': 0.2, 'anomaly_high': 1.1},
    'Refrigerator': {'p_low': 0.8, 'low_range': [10, 20], 'high_range': [0.8, 1.0], 'anomaly_low': 5, 'anomaly_high': 1.1},
    'Smart_Vacuum_Cleaner': {'p_on': 0.2, 'normal_range': [0.7, 1.0], 'anomaly_low': 0.3, 'anomaly_high': 1.1},
}

def record_anomaly(switch_id, timestamp, power_consumption):
    """Record an anomaly in the anomalies table"""
    device = device_dict[switch_id]
    max_power = device['max_power']
    excess = power_consumption - max_power
    
    try:
        cursor.execute("""
        INSERT INTO anomalies 
        (switch_id, device_name, location, timestamp, power_consumption, max_power_rating, excess)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            switch_id,
            device['name'],
            device['location'],
            timestamp,
            power_consumption,
            max_power,
            excess
        ))
        print(f"⚠️ Anomaly recorded for {device['name']} ({switch_id}): {power_consumption}W exceeds {max_power}W")
    except Exception as e:
        print(f"Error recording anomaly: {e}")

# Function to generate power consumption based on device type and max power
def generate_power(device_type, max_power, switch_id, timestamp):
    is_anomaly = False
    power = 0.0
    
    if device_type == 'Refrigerator':
        # Refrigerators are always on, with low or high power modes
        if random.random() < p_anomaly:
            is_anomaly = True
            # Anomalous reading
            if random.random() < 0.5:
                # Too low (e.g., fault causing near-zero usage)
                power = round(random.uniform(0, device_params[device_type]['anomaly_low']), 2)
            else:
                # Too high (e.g., overworking compressor)
                power = round(random.uniform(device_params[device_type]['anomaly_high'] * max_power, 1.5 * max_power), 2)
        else:
            # Normal operation
            if random.random() < device_params[device_type]['p_low']:
                # Low power mode (controls/fan only)
                power = round(random.uniform(device_params[device_type]['low_range'][0], device_params[device_type]['low_range'][1]), 2)
            else:
                # High power mode (compressor running)
                power = round(random.uniform(device_params[device_type]['high_range'][0] * max_power, device_params[device_type]['high_range'][1] * max_power), 2)
    else:
        # Other device types can be on or off
        params = device_params[device_type]
        if random.random() < params['p_on']:
            # Device is on
            if random.random() < p_anomaly:
                is_anomaly = True
                # Anomalous reading when on
                if random.random() < 0.5:
                    # Too low (e.g., malfunction reducing power)
                    power = round(random.uniform(0, params['anomaly_low'] * max_power), 2)
                else:
                    # Too high (e.g., short circuit or overload)
                    power = round(random.uniform(params['anomaly_high'] * max_power, 1.5 * max_power), 2)
            else:
                # Normal reading when on
                power = round(random.uniform(params['normal_range'][0] * max_power, params['normal_range'][1] * max_power), 2)
        else:
            # Device is off
            if random.random() < p_anomaly:
                is_anomaly = True
                # Anomalous reading when off (e.g., leakage current)
                power = round(random.uniform(0.1 * max_power, 0.3 * max_power), 2)
            else:
                # Normal off state
                power = 0.0
    
    # Record anomaly if power exceeds max rating
    if power > max_power:
        record_anomaly(switch_id, timestamp, power)
        
    return power

def transfer_to_historical():
    """
    Transfer the last 24 hours of real-time energy readings to the historical table.
    """
    try:
        # Calculate the timestamp for 24 hours ago
        cutoff_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert data from real_time_energy_readings into historical_energy_readings
        cursor.execute("""
            INSERT OR IGNORE INTO historical_energy_readings (switch_id, timestamp, power_consumption)
            SELECT switch_id, timestamp, power_consumption
            FROM real_time_energy_readings
            WHERE timestamp <= ?
        """, (cutoff_time,))
        
        # Delete transferred data from real_time_energy_readings
        cursor.execute("""
            DELETE FROM real_time_energy_readings
            WHERE timestamp <= ?
        """, (cutoff_time,))
        
        # Commit the transaction
        conn.commit()
        print(f"✅ Successfully transferred data older than {cutoff_time} to historical_energy_readings")
        
    except Exception as e:
        print(f"Error during data transfer: {e}")
        conn.rollback()

# Main loop to continuously insert real-time data
try:
    last_transfer_date = None
    while True:
        # Get current timestamp
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Check if we need to transfer data (at midnight)
        current_date = current_time.date()
        if last_transfer_date != current_date and current_time.hour == 0 and current_time.minute == 0:
            print(f"Initiating daily data transfer at {timestamp}")
            transfer_to_historical()
            last_transfer_date = current_date
        
        # Generate and insert data for each device
        for switch_id, name, location, device_type, max_power in devices:
            power_consumption = generate_power(device_type, max_power, switch_id, timestamp)
            print(f"Generated power consumption for {name} ({switch_id}): {power_consumption} W")
            cursor.execute("INSERT INTO real_time_energy_readings (switch_id, timestamp, power_consumption) VALUES (?, ?, ?)",
                           (switch_id, timestamp, power_consumption))
        
        # Commit the transaction
        conn.commit()
        
        # Wait for 1 minute before the next insertion
        time.sleep(60)

except KeyboardInterrupt:
    print("\nStopping data generation...")
    conn.close()
    print("Database connection closed.")
except Exception as e:
    print(f"Error: {e}")
    conn.close()
    print("Database connection closed due to error.")