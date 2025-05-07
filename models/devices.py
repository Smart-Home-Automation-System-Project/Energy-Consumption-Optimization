from models.database import get_db

def get_devices():
    db=get_db()
    devices=db.execute('SELECT * FROM devices').fetchall()
    return devices

def get_device_by_id(switch_id):
    db=get_db()
    device=db.execute('SELECT * FROM devices WHERE switch_id=?',(switch_id,)).fetchone()
    return device


