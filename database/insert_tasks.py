import sqlite3
from datetime import datetime

conn = sqlite3.connect("database2.db")
cursor = conn.cursor()

# Define the tasks to be inserted (washing machine and dishwasher)
tasks = [
    ("wm_01", "2025-04-27", None, "not_scheduled"),  # Washing Machine task
    ("dw_01", "2025-04-30", None, "not_scheduled"),   # Dishwasher task

]

# Insert tasks into the 'scheduled_tasks' table
cursor.executemany("""
INSERT OR IGNORE INTO scheduled_tasks (switch_id, target_date, scheduled_time, status)
VALUES (?, ?, ?, ?)
""", tasks)

conn.commit()
conn.close()

print("✅ Tasks for Washing Machine and Dishwasher inserted successfully.")
