# Schedules washing machine and dishwasher at the lowest total power consumption time
# of the specified  day of the week based on prophet's power consumption forecasts

import sqlite3
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
ROOT_PATH = os.getenv('ROOT_PATH')
if ROOT_PATH is None:
    raise ValueError("ROOT_PATH not found in .env file")

DB_PATH = os.path.join(ROOT_PATH, "database", "database2.db")

# Check if time is already taken for that day
def is_time_occupied(conn, target_date, timestamp_str):
    result = conn.execute("""
        SELECT COUNT(*) FROM scheduled_tasks
        WHERE target_date = ? AND scheduled_time = ?
    """, (target_date, timestamp_str)).fetchone()
    return result[0] > 0

# Schedule all not_scheduled tasks
def schedule_all_tasks():
    conn = sqlite3.connect(DB_PATH)

    # Get all not_scheduled tasks
    tasks = pd.read_sql_query("""
        SELECT task_id, switch_id, target_date
        FROM scheduled_tasks
        WHERE status = 'not_scheduled'
        ORDER BY target_date ASC
    """, conn)

    if tasks.empty:
        print("✅ No unscheduled tasks.")
        conn.close()
        return

    assigned = 0

    for _, task in tasks.iterrows():
        target_date = task['target_date']

        # Fetch and prepare prediction data for that task's date
        df = pd.read_sql_query("""
            SELECT timestamp, power_consumption
            FROM predictions
            WHERE DATE(timestamp) = ?
            ORDER BY timestamp
        """, conn, params=(target_date,))

        if df.empty:
            print(f"⚠️ No predictions for {target_date}, skipping task {task['task_id']}")
            continue

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['moving_avg'] = df['power_consumption'].rolling(window=24, min_periods=1).mean()
        df = df.sort_values('moving_avg').reset_index(drop=True)

        # Find the first unoccupied timestamp
        for _, row in df.iterrows():
            ts = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            if not is_time_occupied(conn, target_date, ts):
                conn.execute("""
                    UPDATE scheduled_tasks
                    SET scheduled_time = ?, status = 'scheduled'
                    WHERE task_id = ?
                """, (ts, task['task_id']))
                assigned += 1
                print(f"✅ Task {task['task_id']} scheduled at {ts}")
                break

    conn.commit()
    conn.close()
    print(f"🎯 Scheduled {assigned} task(s).")

# Run
if __name__ == "__main__":
    schedule_all_tasks()
