import sqlite3
from datetime import datetime, timedelta
import os

def get_db_connection():
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(script_dir, 'database', 'database.db')
    return sqlite3.connect(db_path)

def get_power_usage_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get today's date at midnight
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    now = datetime.now()
    
    # Calculate average, min, and max power usage
    cursor.execute("""
        SELECT 
            ROUND(AVG(power_consumption), 2) as avg_power,
            ROUND(MIN(power_consumption), 2) as min_power,
            ROUND(MAX(power_consumption), 2) as max_power
        FROM real_time_energy_readings
        WHERE timestamp >= ?
    """, (today.strftime('%Y-%m-%d %H:%M:%S'),))
    
    avg_power, min_power, max_power = cursor.fetchone()
    
    # Calculate daily usage in kWh
    # Assuming readings are taken every minute
    cursor.execute("""
        SELECT ROUND(SUM(power_consumption) / 60000, 2) as daily_kwh
        FROM real_time_energy_readings
        WHERE timestamp >= ?
    """, (today.strftime('%Y-%m-%d %H:%M:%S'),))
    
    daily_kwh = cursor.fetchone()[0]
    
    # Get device level contribution
    cursor.execute("""
        SELECT 
            d.device_type,
            ROUND(SUM(r.power_consumption), 2) as total_power,
            ROUND(COUNT(*) * 100.0 / (
                SELECT COUNT(*) 
                FROM real_time_energy_readings 
                WHERE timestamp >= ?
            ), 2) as percentage
        FROM real_time_energy_readings r
        JOIN devices d ON r.switch_id = d.switch_id
        WHERE r.timestamp >= ?
        GROUP BY d.device_type
        ORDER BY total_power DESC
    """, (today.strftime('%Y-%m-%d %H:%M:%S'), today.strftime('%Y-%m-%d %H:%M:%S')))
    
    device_contributions = cursor.fetchall()
    
    conn.close()
    
    return {
        'average_power': avg_power or 0,
        'min_power': min_power or 0,
        'max_power': max_power or 0,
        'daily_kwh': daily_kwh or 0,
        'device_contributions': [
            {
                'device_type': device_type,
                'total_power': total_power,
                'percentage': percentage
            }
            for device_type, total_power, percentage in device_contributions
        ]
    }

def get_hourly_usage_today():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    cursor.execute("""
        SELECT 
            strftime('%H', timestamp) as hour,
            ROUND(AVG(power_consumption), 2) as avg_power
        FROM real_time_energy_readings
        WHERE timestamp >= ?
        GROUP BY hour
        ORDER BY hour
    """, (today.strftime('%Y-%m-%d %H:%M:%S'),))
    
    hourly_data = cursor.fetchall()
    conn.close()
    
    return {
        'hours': [int(hour) for hour, _ in hourly_data],
        'values': [power for _, power in hourly_data]
    }