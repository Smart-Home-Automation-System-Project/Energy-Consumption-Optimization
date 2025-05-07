import pandas as pd
from prophet import Prophet


class EnergyForecaster:
    def __init__(self, db_access):
        self.db_access = db_access

    def prepare_data_for_prophet(self, device_id=None):
        """Prepare data for Prophet model"""
        df = self.db_access.fetch_energy_readings()

        if device_id:
            df = df[df['switch_id'] == device_id]

        # Group by day and device
        df['date'] = df['timestamp'].dt.date
        daily_data = df.groupby(['switch_id', 'date'])['power_watts'].mean().reset_index()

        # Format for Prophet (requires 'ds' and 'y' columns)
        result = {}
        for device_id in daily_data['switch_id'].unique():
            device_data = daily_data[daily_data['switch_id'] == device_id].copy()
            device_data['ds'] = pd.to_datetime(device_data['date'])
            device_data['y'] = device_data['power_watts']
            result[device_id] = device_data[['ds', 'y']]

        return result

    def train_forecast_models(self):
        """Train Prophet models for each device"""
        device_data = self.prepare_data_for_prophet()
        models = {}
        forecasts = {}

        for device_id, data in device_data.items():
            if len(data) > 5:  # Need sufficient data points
                # Initialize and train Prophet model
                model = Prophet(
                    daily_seasonality=True,
                    weekly_seasonality=True,
                    changepoint_prior_scale=0.05
                )
                model.fit(data)

                # Generate forecast for next 7 days
                future = model.make_future_dataframe(periods=7, freq='D')
                forecast = model.predict(future)

                models[device_id] = model
                forecasts[device_id] = forecast

        return models, forecasts

    def identify_optimal_operation_times(self):
        """Identify optimal operation times based on forecasted data"""
        # Get forecasts for all devices
        _, forecasts = self.train_forecast_models()

        # Determine optimal times for each device
        optimal_times = []
        for device_id, forecast in forecasts.items():
            # Find the day with the lowest forecasted power consumption
            min_power_day = forecast.loc[forecast['yhat'] == forecast['yhat'].min()]
            optimal_times.append({
                'device_id': device_id,
                'optimal_time': min_power_day['ds'].iloc[0],  # The date with the lowest forecasted power
                'predicted_power': min_power_day['yhat'].iloc[0]
            })

        return optimal_times
