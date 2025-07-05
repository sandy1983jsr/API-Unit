import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def show_dashboard(data, kpis):
    st.header("📊 Real-time Dashboards")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Yield vs Ideal Batch")
        fig = px.line(
            data, x="BatchID", y="Crystallizer_Yield", color="Product",
            title="Crystallizer Yield (%)")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Energy Use per kg API")
        energy_per_kg = (data["Dryer_Energy_kWh"] + data["Distillation_Energy_kWh"] +
                         data["Chiller_Energy_kWh"] + data["HVAC_Energy_kWh"] +
                         data["Vacuum_Energy_kWh"]) / data["Batch_Throughput_kg"]
        fig = px.bar(
            x=data["BatchID"], y=energy_per_kg,
            labels={"x": "BatchID", "y": "Energy (kWh/kg)"},
            title="Total Energy Use per kg API")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("KPI Summary (Bar Chart)")
    _plot_kpi_bar(kpis)
    st.subheader("KPI Comparison (Radar Chart)")
    _plot_kpi_radar(kpis)

def _plot_kpi_bar(kpis):
    # Flatten the KPI dictionary for bar chart
    categories = []
    values = []
    for area, area_kpi in kpis.items():
        for k, v in area_kpi.items():
            categories.append(f"{area}: {k}")
            values.append(float(v))
    fig = px.bar(x=categories, y=values, labels={"x": "KPI", "y": "Value"})
    st.plotly_chart(fig, use_container_width=True)

def _plot_kpi_radar(kpis):
    # Pick common KPIs for the radar
    radar_kpis = {}
    for area, area_kpi in kpis.items():
        for k, v in area_kpi.items():
            radar_kpis[f"{area}-{k}"] = float(v)
    categories = list(radar_kpis.keys())
    values = list(radar_kpis.values())
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],  # Close the loop
        theta=categories + [categories[0]],
        fill='toself'))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        title="KPI Radar Chart"
    )
    st.plotly_chart(fig, use_container_width=True)
