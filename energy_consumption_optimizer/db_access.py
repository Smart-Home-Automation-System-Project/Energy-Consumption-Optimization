import sqlite3
import pandas as pd


class EnergyDatabaseAccess:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def fetch_all_devices(self):
        """Get all registered devices from the database"""
        conn = self.get_connection()
        query = "SELECT switch_id, name, location, device_type, max_power_rating FROM devices"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def fetch_energy_readings(self, days=30):
        """Get energy readings for the specified period"""
        conn = self.get_connection()
        query = f"""
        SELECT er.switch_id, d.name, d.location, d.device_type, 
               er.timestamp, er.power_watts, er.voltage, er.current
        FROM energy_readings er
        JOIN devices d ON er.switch_id = d.switch_id
        WHERE datetime(er.timestamp) >= datetime('now', '-{days} days')
        ORDER BY er.timestamp
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df

    def save_optimization_results(self, results):
        """Save optimization suggestions to a new table"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS energy_optimization (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            switch_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            optimization_type TEXT NOT NULL,
            description TEXT NOT NULL,
            estimated_savings REAL,
            FOREIGN KEY (switch_id) REFERENCES devices(switch_id)
        )
        """)

        # Insert optimization results
        cursor.executemany("""
        INSERT INTO energy_optimization 
        (switch_id, timestamp, optimization_type, description, estimated_savings)
        VALUES (?, ?, ?, ?, ?)
        """, results)

        conn.commit()
        conn.close()
