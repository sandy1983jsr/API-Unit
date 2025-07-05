import streamlit as st
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
    st.subheader("KPIs Summary")
    st.json(kpis)
