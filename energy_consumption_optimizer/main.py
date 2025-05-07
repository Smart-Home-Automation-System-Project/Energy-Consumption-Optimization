from db_access import EnergyDatabaseAccess
from forecaster import EnergyForecaster
from flink_processor import FlinkEnergyProcessor
from optimization_engine import EnergyOptimizationEngine

def main():
    print("Starting Energy Consumption Optimizer...")

    # Initialize database access
    db_access = EnergyDatabaseAccess()

    # Initialize forecaster and flink processor
    forecaster = EnergyForecaster(db_access)
    flink_processor = FlinkEnergyProcessor(db_access)

    # Create optimization engine
    engine = EnergyOptimizationEngine(db_access, forecaster, flink_processor)

    # Generate and save all optimizations
    optimizations = engine.generate_all_optimizations()

    print(f"Generated {len(optimizations)} energy optimization recommendations")

    # Print some example optimizations
    if optimizations:
        print("\nExample recommendations:")
        for i, opt in enumerate(optimizations[:5]):
            print(f"{i+1}. Device ID: {opt['device_id']} - Optimal time: {opt['optimal_time']} (Predicted power: {opt['predicted_power']}W)")

    print("\nEnergy optimization completed. Results saved to database.")

if __name__ == "__main__":
    main()
