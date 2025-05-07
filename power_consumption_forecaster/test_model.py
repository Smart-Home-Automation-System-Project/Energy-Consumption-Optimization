import os
import sqlite3
import pandas as pd
from prophet import Prophet
import joblib
from dotenv import load_dotenv
from datetime import datetime, timedelta
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load environment variables
load_dotenv()

# Determine absolute ROOT_PATH (go one level up from this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DB_PATH = os.path.join(ROOT_PATH, "database", "database.db")

def load_data():
    print("Loading data...")
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT timestamp, SUM(power_consumption) AS total_power
    FROM historical_energy_readings
    GROUP BY timestamp
    ORDER BY timestamp
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def split_data(df):
    print("Splitting data into train and test sets...")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Get the last 7 days for testing
    cutoff_date = df['timestamp'].max() - timedelta(days=7)
    
    train_df = df[df['timestamp'] <= cutoff_date].copy()
    test_df = df[df['timestamp'] > cutoff_date].copy()
    
    return train_df, test_df

def prepare_data(df):
    print("Preparing data...")
    df = df.rename(columns={'timestamp': 'ds', 'total_power': 'y'})
    df['day_of_week'] = df['ds'].dt.dayofweek
    return df

def train_and_predict(train_df, test_df):
    print("Training model and making predictions...")
    # Train model
    model = Prophet()
    model.add_regressor('day_of_week')
    model.fit(train_df)
    
    # Make predictions for test period
    future_df = model.make_future_dataframe(periods=len(test_df), freq='30min')
    future_df['day_of_week'] = future_df['ds'].dt.dayofweek
    forecast_df = model.predict(future_df)
    
    # Get predictions for test period only
    predictions = forecast_df[forecast_df['ds'].isin(test_df['ds'])][['ds', 'yhat']]
    actual = test_df[['ds', 'y']]
    
    return predictions, actual

def calculate_metrics(predictions, actual):
    print("Calculating accuracy metrics...")
    mae = mean_absolute_error(actual['y'], predictions['yhat'])
    rmse = np.sqrt(mean_squared_error(actual['y'], predictions['yhat']))
    r2 = r2_score(actual['y'], predictions['yhat'])
    
    print("\nModel Performance Metrics:")
    print(f"Mean Absolute Error: {mae:.2f} watts")
    print(f"Root Mean Square Error: {rmse:.2f} watts")
    print(f"R² Score: {r2:.4f}")
    
    return mae, rmse, r2

def plot_results(predictions, actual):
    print("Generating plot...")
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 6))
    plt.plot(actual['ds'], actual['y'], label='Actual', color='blue')
    plt.plot(predictions['ds'], predictions['yhat'], label='Predicted', color='red')
    plt.title('Power Consumption: Actual vs Predicted')
    plt.xlabel('Time')
    plt.ylabel('Power Consumption (watts)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot
    plot_path = os.path.join(SCRIPT_DIR, "model_test_results.png")
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

def main():
    # Load and prepare data
    df = load_data()
    if df.empty:
        print("No data returned from the database.")
        return
    
    train_df, test_df = split_data(df)
    train_df = prepare_data(train_df)
    test_df = prepare_data(test_df)
    
    # Train model and get predictions
    predictions, actual = train_and_predict(train_df, test_df)
    
    # Calculate and display metrics
    calculate_metrics(predictions, actual)
    
    # Plot results
    plot_results(predictions, actual)

if __name__ == "__main__":
    main()