def export_realtime_data():
    import sqlite3
    import csv
    import os
    from dotenv import load_dotenv

    load_dotenv()
    ROOT_PATH = os.getenv("ROOT_PATH")

    db_path = os.path.join(ROOT_PATH, "database", "database2.db")
    csv_path = os.path.join(ROOT_PATH, "realtime_simulated.csv")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT switch_id, timestamp, power_consumption FROM real_time_energy_readings")
    data = cursor.fetchall()

    with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["switch_id", "timestamp", "power_consumption"])
        writer.writerows(data)

    conn.close()
    print(f"✅ Exported {len(data)} rows to {csv_path}")

# Allow script to be run directly
if __name__ == "__main__":
    export_realtime_data()