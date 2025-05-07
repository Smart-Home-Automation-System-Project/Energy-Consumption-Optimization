from models.database import get_db
import pandas as pd


def get_predictions():
    db = get_db()
    predictions = db.execute(
        'SELECT timestamp, power_consumption FROM predictions ORDER BY timestamp'
    ).fetchall()

    return predictions


def get_todays_predictions():
    db = get_db()
    predictions = db.execute(
        'SELECT timestamp, power_consumption FROM predictions WHERE DATE(timestamp) = DATE("now") ORDER BY timestamp'
    ).fetchall()

    return predictions


def get_hourly_average():
    db = get_db()
    predictions = db.execute('''
        SELECT
            strftime('%H', timestamp) as hour,
            AVG(power_consumption) as avg_power
        FROM predictions
        WHERE DATE(timestamp) = DATE("now")
        GROUP BY strftime('%H', timestamp)
        ORDER BY hour
    ''').fetchall()

    return predictions