def compute_kpis(reactor, dryer, sru, utility):
    kpis = {}
    kpis["Reactor"] = reactor.get_kpi()
    kpis["Dryer"] = dryer.get_kpi()
    kpis["Solvent Recovery"] = sru.get_kpi()
    kpis["Utilities"] = utility.get_energy_dashboard()
    return kpis
