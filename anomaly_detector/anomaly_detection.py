# anomaly_detection.py
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import MapFunction, FlatMapFunction
import os
import json
import csv
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")
DB_PATH = os.path.join(ROOT_PATH, "database", "database2.db")


class DeviceInfo:
    def __init__(self, switch_id, name, location, device_type, max_power_rating):
        self.switch_id = switch_id
        self.name = name
        self.location = location
        self.device_type = device_type
        self.max_power_rating = float(max_power_rating)


class EnergyReading:
    def __init__(self, switch_id, timestamp, power_consumption):
        self.switch_id = switch_id
        self.timestamp = timestamp
        self.power_consumption = float(power_consumption)


class AnomalyDetector(FlatMapFunction):
    def __init__(self, devices_dict):
        self.devices = devices_dict

    def flat_map(self, value):
        result = []
        reading = value
        if reading.switch_id in self.devices:
            device = self.devices[reading.switch_id]
            if reading.power_consumption > device.max_power_rating:
                anomaly_record = {
                    "switch_id": reading.switch_id,
                    "device_name": device.name,
                    "location": device.location,
                    "timestamp": reading.timestamp,
                    "power_consumption": reading.power_consumption,
                    "max_power_rating": device.max_power_rating,
                    "excess": reading.power_consumption - device.max_power_rating
                }

                # Store in database
                store_anomaly(anomaly_record)

                result.append(json.dumps(anomaly_record))
        return result


class CSVToEnergyReading(MapFunction):
    def map(self, value):
        csv_line = value
        parts = csv_line.split(',')
        if len(parts) >= 3 and parts[0] != 'switch_id':
            return EnergyReading(parts[0], parts[1], parts[2])
        return None


def load_devices():
    devices = {}
    with open(os.path.join(ROOT_PATH, "devices.csv"), 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 5:
                device = DeviceInfo(row[0], row[1], row[2], row[3], row[4])
                devices[row[0]] = device
    return devices


def store_anomaly(anomaly):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO anomalies 
        (switch_id, device_name, location, timestamp, power_consumption, max_power_rating, excess)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            anomaly["switch_id"],
            anomaly["device_name"],
            anomaly["location"],
            anomaly["timestamp"],
            anomaly["power_consumption"],
            anomaly["max_power_rating"],
            anomaly["excess"]
        ))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error storing anomaly: {e}")


def main():
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    # Load device information for anomaly detection
    devices_dict = load_devices()
    print(f"Loaded {len(devices_dict)} devices for anomaly detection")

    # Create a source from the CSV file
    input_path = os.path.join(ROOT_PATH, "realtime_simulated.csv")

    # Read the CSV file
    data_stream = env.read_text_file(input_path)

    # Transform CSV lines to EnergyReading objects and filter out header/invalid lines
    readings = data_stream \
        .map(CSVToEnergyReading()) \
        .filter(lambda x: x is not None)

    # Detect anomalies where power consumption exceeds max rating
    anomalies = readings \
        .flat_map(AnomalyDetector(devices_dict))

    # Output anomalies to console
    # anomalies.print()

    # Execute the job
    env.execute("Energy Consumption Anomaly Detection")


if __name__ == "__main__":
    main()