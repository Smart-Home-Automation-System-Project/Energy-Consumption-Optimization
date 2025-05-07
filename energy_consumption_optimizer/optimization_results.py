class OptimizationResult:
    def __init__(self, switch_id, timestamp, optimization_type, description, estimated_savings):
        self.switch_id = switch_id
        self.timestamp = timestamp
        self.optimization_type = optimization_type
        self.description = description
        self.estimated_savings = estimated_savings
