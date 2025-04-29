def export_devices():
    import sqlite3
    import csv
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()
    ROOT_PATH = os.getenv("ROOT_PATH")

    # Database and output paths
    db_path = os.path.join(ROOT_PATH, "database", "database2.db")
    csv_path = os.path.join(ROOT_PATH, "devices.csv")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the devices table
    cursor.execute("SELECT switch_id, name, location, device_type, max_power_rating FROM devices")
    devices_data = cursor.fetchall()

    # Write to CSV
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["switch_id", "name", "location", "device_type", "max_power_rating"])
        writer.writerows(devices_data)

    # Cleanup
    conn.close()
    print(f"✅ Exported {len(devices_data)} devices to {csv_path}")

# Allow script to be run directly
if __name__ == "__main__":
    export_devices()