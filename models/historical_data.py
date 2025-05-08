from models.database import get_db
import pandas as pd
from datetime import datetime, timedelta

class HistoricalData:
    @staticmethod
    def get_total_consumption(start_date=None, end_date=None):
        """Get total historical energy consumption data"""
        conn = get_db()
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        query = """
            SELECT 
                date(timestamp) as date, 
                SUM(power_consumption) / 1000.0 as total_consumption
            FROM historical_energy_readings
            WHERE date(timestamp) BETWEEN ? AND ?
            GROUP BY date(timestamp)
            ORDER BY date(timestamp)
        """
        df = pd.read_sql_query(query, conn, params=[start_date, end_date])
        conn.close()
        return df.to_dict('records')

    @staticmethod
    def get_consumption_by_device(start_date=None, end_date=None):
        """Get historical power_consumption data per device"""
        conn = get_db()
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        query = """
            SELECT 
                date(her.timestamp) as date,
                her.switch_id,
                d.name as device_name,
                d.location,
                d.device_type,
                d.max_power_rating,
                SUM(her.power_consumption) / 1000.0 as energy_consumption
            FROM historical_energy_readings her
            JOIN devices d ON her.switch_id = d.switch_id
            WHERE date(her.timestamp) BETWEEN ? AND ?
            GROUP BY date(her.timestamp), her.switch_id, d.name
            ORDER BY date(her.timestamp), her.switch_id
        """
        df = pd.read_sql_query(query, conn, params=[start_date, end_date])
        conn.close()
        return df.to_dict('records') 