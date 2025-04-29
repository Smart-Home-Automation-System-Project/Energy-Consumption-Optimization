import os
import sqlite3
import pandas as pd
from prophet import Prophet
import joblib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine absolute ROOT_PATH (go one level up from this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

def load_data():
    print("Loading data...")
    db_path = os.path.join(ROOT_PATH, "database", "database2.db")
    conn = sqlite3.connect(db_path)
    query = """
    SELECT timestamp, SUM(power_consumption) AS total_power
    FROM historical_energy_readings
    GROUP BY timestamp
    ORDER BY timestamp
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def prepare_data(df):
    print("Preparing data...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.rename(columns={'timestamp': 'ds', 'total_power': 'y'})
    df = df.dropna()
    print(df.head())
    return df

def train_prophet_model(df):
    print("Training Prophet model...")
    model = Prophet()
    model.fit(df)
    return model

def save_model(model):
    model_path = os.path.join(SCRIPT_DIR, "model.pkl")  # model.pkl will be saved in the same folder
    print(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)

def main():
    df = load_data()
    if df.empty:
        print("No data returned from the database.")
        return
    prepared_df = prepare_data(df)
    model = train_prophet_model(prepared_df)
    save_model(model)
    print("✅ Model training complete.")

if __name__ == "__main__":
    main()
