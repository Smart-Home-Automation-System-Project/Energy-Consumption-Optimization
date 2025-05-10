import unittest
import sys
import os
from datetime import datetime
import numpy as np

# Add the parent directory to sys.path to import the module
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from database.generate_historical_data import simulate_usage

class TestGenerateHistoricalData(unittest.TestCase):
    
    def setUp(self):
        # Set a fixed seed for reproducible tests
        np.random.seed(42)
        self.weekend_time = datetime(2023, 1, 7, 20, 0)  # Saturday 8 PM
        self.weekday_time = datetime(2023, 1, 4, 20, 0)  # Wednesday 8 PM
    
    def test_garden_light_usage(self):
        # Test garden light in evening hours
        result = simulate_usage(
            "B_08", "Light", 100, 20, "Garden", self.weekend_time
        )
        # Garden lights should be on during evening hours
        self.assertGreater(result, 0)
        
        # Test garden light during day hours
        result = simulate_usage(
            "B_08", "Light", 100, 14, "Garden", self.weekend_time
        )
        # Garden lights should be off during day hours
        self.assertEqual(result, 0)
    
    def test_living_room_ac_usage(self):
        # Test living room AC in evening hours
        result = simulate_usage(
            "ac_04", "AC", 700, 22, "Living_Room", self.weekend_time
        )
        # Living room AC should be on during evening hours
        self.assertGreater(result, 0)
    
    def test_refrigerator_always_on(self):
        # Test refrigerator is always consuming power
        result = simulate_usage(
            "rf_01", "Refrigerator", 200, 12, "Kitchen", self.weekday_time
        )
        # Refrigerator should always have non-zero power
        self.assertGreater(result, 0)

if __name__ == '__main__':
    unittest.main()