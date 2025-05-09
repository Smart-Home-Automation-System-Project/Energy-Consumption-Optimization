import os
import time
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
from email_service.emailservice import send_email

# Load environment variables
load_dotenv()
ROOT_PATH = os.getenv("ROOT_PATH")
DB_PATH = os.path.join(ROOT_PATH, "database", "database.db")

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def check_anomalies():
    """Check for devices with high anomaly counts in the past 12 hours"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Calculate timestamp for 12 hours ago
        twelve_hours_ago = (datetime.now() - timedelta(hours=12)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Query to get devices with more than 20 anomalies in the past 12 hours
        query = """
        SELECT 
            device_name,
            COUNT(*) as anomaly_count,
            SUM(excess) as total_excess,
            MAX(timestamp) as latest_anomaly
        FROM anomalies
        WHERE timestamp >= ?
        GROUP BY device_name
        HAVING COUNT(*) >= 20
        """
        
        cursor.execute(query, (twelve_hours_ago,))
        results = cursor.fetchall()
        
        # Send email for each device with high anomaly count
        for device_name, anomaly_count, total_excess, latest_anomaly in results:
            try:
                # Check if we've already sent an alert for this device in the past 12 hours
                check_query = """
                SELECT COUNT(*) 
                FROM email_alerts 
                WHERE device_name = ? AND timestamp >= ?
                """
                cursor.execute(check_query, (device_name, twelve_hours_ago))
                alert_count = cursor.fetchone()[0]
                
                if alert_count == 0:  # Only send if no alert has been sent in the past 12 hours
                    # Send email alert
                    send_email(
                        receiver_name="System Administrator",
                        receiver_email="dasunpramodya616@gmail.com",
                        device_name=device_name,
                        anomaly_count=anomaly_count,
                        power_excess=total_excess
                    )
                    
                    # Record the email alert
                    cursor.execute("""
                    INSERT INTO email_alerts (device_name, timestamp, anomaly_count, total_excess)
                    VALUES (?, ?, ?, ?)
                    """, (device_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                         anomaly_count, total_excess))
                    conn.commit()
                    
                    print(f"Alert sent for {device_name} with {anomaly_count} anomalies")
            except Exception as e:
                print(f"Error sending alert for {device_name}: {e}")
                
    except Exception as e:
        print(f"Error checking anomalies: {e}")
    finally:
        conn.close()

def create_email_alerts_table():
    """Create the email_alerts table if it doesn't exist"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            anomaly_count INTEGER NOT NULL,
            total_excess REAL NOT NULL
        )
        """)
        
        conn.commit()
        print("Email alerts table created successfully")
    except Exception as e:
        print(f"Error creating email alerts table: {e}")
    finally:
        conn.close()

def main():
    print("Starting anomaly monitoring service...")
    
    # Create email alerts table if it doesn't exist
    create_email_alerts_table()
    
    # Continuous monitoring loop
    while True:
        try:
            check_anomalies()
            # Wait for 5 minutes before next check
            time.sleep(300)
        except KeyboardInterrupt:
            print("\nStopping anomaly monitoring service...")
            break
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            # Wait for 1 minute before retrying in case of error
            time.sleep(60)

if __name__ == "__main__":
    main() 