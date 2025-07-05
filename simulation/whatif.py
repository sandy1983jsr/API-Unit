import streamlit as st
import numpy as np

def run_whatif(data, reactor, dryer, sru, utility):
    st.subheader("Change a parameter and observe the impact (simple demo)")
    param = st.selectbox("Parameter to modify:", [
        "Reactor_Temp", "Dryer_Time", "SRU_Solvent_In_kg", "Boiler_Steam_kg"
    ])
    factor = st.slider("Change factor (%)", 50, 150, 100)
    data_mod = data.copy()
    data_mod[param] = data_mod[param] * (factor / 100)
    # Recompute KPIs
    from models.reactor import ReactorTwin
    from models.dryer import DryerTwin
    from models.sru import SRUTwin
    from models.utility import UtilityTwin
    from processing.kpi import compute_kpis
    kpis_mod = compute_kpis(
        ReactorTwin(data_mod),
        DryerTwin(data_mod),
        SRUTwin(data_mod),
        UtilityTwin(data_mod)
    )
    st.write("Modified KPIs:")
    st.json(kpis_mod)
