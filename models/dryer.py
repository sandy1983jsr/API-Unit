class DryerTwin:
    def __init__(self, data):
        self.time = data["Dryer_Time"]
        self.energy = data["Dryer_Energy_kWh"]
        self.batch_ids = data["BatchID"]

    def predict_drying_time(self):
        return self.time.mean()  # Placeholder for ML model

    def get_kpi(self):
        return {
            "Avg Drying Time": self.time.mean(),
            "Avg Energy": self.energy.mean()
        }
