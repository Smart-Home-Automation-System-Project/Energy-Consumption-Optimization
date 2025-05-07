from models.database import get_db
from datetime import datetime, timedelta


def get_scheduled_tasks():
    db = get_db()
    tasks = db.execute('''
        SELECT st.task_id, st.switch_id, d.name as device_name, 
               st.target_date, st.scheduled_time, st.status
        FROM scheduled_tasks st
        JOIN devices d ON st.switch_id = d.switch_id
        ORDER BY st.target_date, st.scheduled_time
    ''').fetchall()

    return tasks


def get_available_devices():
    db = get_db()
    devices = db.execute('''
        SELECT switch_id, name 
        FROM devices 
        WHERE device_type IN ('Washing Machine', 'Dishwasher')
    ''').fetchall()

    return devices


def schedule_task(switch_id, target_date):
    db = get_db()
    db.execute('''
        INSERT INTO scheduled_tasks (switch_id, target_date, status)
        VALUES (?, ?, 'not_scheduled')
    ''', (switch_id, target_date))
    db.commit()
    return True