from pyflink.datastream.functions import MapFunction


class StandbyPowerDetector(MapFunction):
    """Detects devices consuming power in standby mode"""

    def __init__(self, standby_thresholds):
        self.standby_thresholds = standby_thresholds

    def map(self, reading):
        device_type = reading['device_type']
        power = reading['power_watts']
        threshold = self.standby_thresholds.get(device_type, 10)

        if 0 < power < threshold:
            return {
                'switch_id': reading['switch_id'],
                'timestamp': reading['timestamp'],
                'optimization_type': 'Standby Power',
                'description': f"{reading['name']} consuming {power}W in standby mode. Consider unplugging.",
                'estimated_savings': power * 24 * 0.3  # 30% of daily standby consumption
            }
        return None


class AnomalyDetector(MapFunction):
    """Detects abnormal power consumption"""

    def __init__(self, normal_ranges):
        self.normal_ranges = normal_ranges

    def map(self, reading):
        device_type = reading['device_type']
        power = reading['power_watts']
        min_power, max_power = self.normal_ranges.get(device_type, (0, 2000))

        if power > max_power * 1.2:  # 20% above normal maximum
            return {
                'switch_id': reading['switch_id'],
                'timestamp': reading['timestamp'],
                'optimization_type': 'Anomaly',
                'description': f"{reading['name']} consuming abnormal power: {power}W vs expected max {max_power}W",
                'estimated_savings': (power - max_power) * 2  # Savings from fixing the issue
            }
        return None
