class SRUTwin:
    def __init__(self, data):
        self.solvent_in = data["SRU_Solvent_In_kg"]
        self.solvent_out = data["SRU_Solvent_Out_kg"]
        self.cod = data["ETP_COD_mgL"]
        self.water_reused = data["ZLD_Water_Reused_m3"]
        self.batch_ids = data["BatchID"]

    def recovery_efficiency(self):
        return (self.solvent_out / self.solvent_in).mean() * 100

    def get_kpi(self):
        return {
            "Solvent Recovery (%)": self.recovery_efficiency(),
            "Avg COD": self.cod.mean(),
            "Water Reused": self.water_reused.mean()
        }
