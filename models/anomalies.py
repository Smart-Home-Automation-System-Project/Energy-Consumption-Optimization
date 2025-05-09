import sqlite3
from datetime import datetime, timedelta
import os

def get_db_connection():
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(script_dir, 'database', 'database.db')
    return sqlite3.connect(db_path)

def get_recent_anomalies():
    """Get anomalies from the past hour for all devices"""
    conn = get_db_connection()
    try:
        one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        
        query = """
        SELECT 
            a.switch_id,
            a.device_name,
            a.location,
            a.timestamp,
            a.power_consumption,
            a.max_power_rating,
            a.excess,
            COUNT(*) as anomaly_count
        FROM anomalies a
        WHERE a.timestamp >= ?
        GROUP BY a.switch_id
        ORDER BY anomaly_count DESC, a.timestamp DESC
        """
        
        cursor.execute(query, (one_hour_ago,))
        anomalies = cursor.fetchall()
        
        # Convert to list of dictionaries for easier handling in templates
        result = []
        for row in anomalies:
            result.append({
                'switch_id': row[0],
                'device_name': row[1],
                'location': row[2],
                'timestamp': row[3],
                'power_consumption': round(row[4], 2),
                'max_power_rating': round(row[5], 2),
                'excess': round(row[6], 2),
                'anomaly_count': row[7]
            })
        
        return result
    except Exception as e:
        print(f"Error fetching recent anomalies: {e}")
        return []
    finally:
        conn.close() 