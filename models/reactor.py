class ReactorTwin:
    def __init__(self, data):
        self.temp = data["Reactor_Temp"]
        self.agitation = data["Reactor_Agitation"]
        self.time = data["Reactor_Time"]
        self.throughput = data["Batch_Throughput_kg"]
        self.batch_ids = data["BatchID"]

    def get_heat_map(self):
        return (self.temp * self.agitation * self.time) / 1000

    def get_kpi(self):
        return {
            "Avg Temp": self.temp.mean(),
            "Avg Agitation": self.agitation.mean(),
            "Avg Time": self.time.mean(),
            "Energy Use": self.get_heat_map().mean()
        }
