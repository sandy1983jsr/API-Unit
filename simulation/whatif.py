import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

    st.subheader("Modified vs Baseline KPIs (Bar Chart)")
    _compare_kpi_bars(reactor, dryer, sru, utility, data, kpis_mod)

    st.subheader("Modified vs Baseline KPIs (Radar Chart)")
    _compare_kpi_radar(reactor, dryer, sru, utility, data, kpis_mod)

def _compare_kpi_bars(reactor, dryer, sru, utility, data, kpis_mod):
    from processing.kpi import compute_kpis
    kpis_base = compute_kpis(reactor, dryer, sru, utility)

    categories = []
    base_values = []
    mod_values = []
    for area in kpis_base:
        for k in kpis_base[area]:
            categories.append(f"{area}: {k}")
            base_values.append(float(kpis_base[area][k]))
            mod_values.append(float(kpis_mod[area][k]))

    fig = go.Figure(data=[
        go.Bar(name='Baseline', x=categories, y=base_values),
        go.Bar(name='Modified', x=categories, y=mod_values)
    ])
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

def _compare_kpi_radar(reactor, dryer, sru, utility, data, kpis_mod):
    from processing.kpi import compute_kpis
    kpis_base = compute_kpis(reactor, dryer, sru, utility)

    base_radar = {}
    mod_radar = {}
    for area in kpis_base:
        for k in kpis_base[area]:
            label = f"{area}-{k}"
            base_radar[label] = float(kpis_base[area][k])
            mod_radar[label] = float(kpis_mod[area][k])

    categories = list(base_radar.keys())
    base_values = list(base_radar.values())
    mod_values = list(mod_radar.values())

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=base_values + [base_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name="Baseline"
    ))
    fig.add_trace(go.Scatterpolar(
        r=mod_values + [mod_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name="Modified"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title="KPI Radar Chart"
    )
    st.plotly_chart(fig, use_container_width=True)
