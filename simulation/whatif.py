import streamlit as st
import numpy as np
import plotly.express as px

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

    # Calculate baseline KPIs for comparison
    from processing.kpi import compute_kpis
    kpis_base = compute_kpis(reactor, dryer, sru, utility)

    st.markdown("## Modified vs Baseline KPIs (Unit-wise)")

    # Helper to plot comparison for a KPI group
    def plot_kpi_comparison(title, kpi_dict_base, kpi_dict_mod):
        metrics = list(kpi_dict_base.keys())
        baseline = [kpi_dict_base[m] for m in metrics]
        modified = [kpi_dict_mod[m] for m in metrics]
        fig = px.bar(
            x=metrics*2, y=baseline+modified,
            color=["Baseline"]*len(metrics) + ["Modified"]*len(metrics),
            barmode='group', labels={'x': 'Metric', 'y': 'Value', 'color': 'Scenario'},
            title=title
        )
        st.plotly_chart(fig, use_container_width=True)

    # Reactor
    st.subheader("Reactor KPIs")
    plot_kpi_comparison("Reactor KPIs", kpis_base["Reactor"], kpis_mod["Reactor"])

    # Dryer
    st.subheader("Dryer KPIs")
    plot_kpi_comparison("Dryer KPIs", kpis_base["Dryer"], kpis_mod["Dryer"])

    # Solvent Recovery
    st.subheader("Solvent Recovery & ETP KPIs")
    plot_kpi_comparison("Solvent Recovery & ETP KPIs", kpis_base["Solvent Recovery"], kpis_mod["Solvent Recovery"])

    # Utilities (each separately)
    for util_name in kpis_base["Utilities"]:
        st.subheader(f"{util_name} (Utilities)")
        plot_kpi_comparison(
            util_name,
            {util_name: kpis_base["Utilities"][util_name]},
            {util_name: kpis_mod["Utilities"][util_name]}
        )
