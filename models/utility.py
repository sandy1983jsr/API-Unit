class UtilityTwin:
    def __init__(self, data):
        self.boiler = data["Boiler_Steam_kg"]
        self.chiller = data["Chiller_Energy_kWh"]
        self.hvac = data["HVAC_Energy_kWh"]
        self.vacuum = data["Vacuum_Energy_kWh"]
        self.batch_ids = data["BatchID"]

    def get_energy_dashboard(self):
        return {
            "Boiler Steam (kg)": self.boiler.sum(),
            "Chiller Energy (kWh)": self.chiller.sum(),
            "HVAC Energy (kWh)": self.hvac.sum(),
            "Vacuum Energy (kWh)": self.vacuum.sum()
        }
