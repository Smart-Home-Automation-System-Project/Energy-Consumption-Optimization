# def export_devices():
#     import sqlite3
#     import csv
#     import os
    
#     # Database and output paths
#     db_path = os.path.join(os.path.dirname(__file__), "database.db")
#     csv_path = os.path.join(os.path.dirname(__file__), "devices.csv")
    
#     # Connect to the SQLite database
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Query the devices table
#     cursor.execute("SELECT switch_id, name, location, device_type, max_power_rating FROM devices")
#     devices_data = cursor.fetchall()

#     # Write to CSV
#     with open(csv_path, mode="w", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow(["switch_id", "name", "location", "device_type", "max_power_rating"])
#         writer.writerows(devices_data)

#     # Cleanup
#     conn.close()
#     print(f"✅ Exported {len(devices_data)} devices to {csv_path}")

# # Allow script to be run directly
# if __name__ == "__main__":
#     export_devices()