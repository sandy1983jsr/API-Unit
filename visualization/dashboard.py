import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show_dashboard(data, kpis):
    st.header("📊 Real-time Dashboards")

    # Reactor KPIs
    with st.container():
        st.subheader("Reactor KPIs")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg Temp (°C)", f"{kpis['Reactor']['Avg Temp']:.1f}")
        col2.metric("Avg Agitation (rpm)", f"{kpis['Reactor']['Avg Agitation']:.0f}")
        col3.metric("Avg Time (hr)", f"{kpis['Reactor']['Avg Time']:.2f}")
        col4.metric("Energy Use (arb)", f"{kpis['Reactor']['Energy Use']:.2f}")
        st.caption("Batchwise Temperature Profile")
        fig = px.line(data, x="BatchID", y="Reactor_Temp", title="Reactor Temperature per Batch")
        st.plotly_chart(fig, use_container_width=True)
    
    # Dryer KPIs
    with st.container():
        st.subheader("Dryer KPIs")
        col1, col2 = st.columns(2)
        col1.metric("Avg Drying Time (hr)", f"{kpis['Dryer']['Avg Drying Time']:.2f}")
        col2.metric("Avg Dryer Energy (kWh)", f"{kpis['Dryer']['Avg Energy']:.2f}")
        st.caption("Dryer Energy Use per Batch")
        fig2 = px.bar(data, x="BatchID", y="Dryer_Energy_kWh", title="Dryer Energy (kWh) per Batch")
        st.plotly_chart(fig2, use_container_width=True)

    # Solvent Recovery & ETP KPIs
    with st.container():
        st.subheader("Solvent Recovery & ETP KPIs")
        col1, col2, col3 = st.columns(3)
        col1.metric("Solvent Recovery (%)", f"{kpis['Solvent Recovery']['Solvent Recovery (%)']:.2f}")
        col2.metric("Avg COD (mg/L)", f"{kpis['Solvent Recovery']['Avg COD']:.1f}")
        col3.metric("Water Reused (m³)", f"{kpis['Solvent Recovery']['Water Reused']:.2f}")
        st.caption("Solvent In/Out per Batch")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=data["BatchID"], y=data["SRU_Solvent_In_kg"], name="Solvent In"))
        fig3.add_trace(go.Bar(x=data["BatchID"], y=data["SRU_Solvent_Out_kg"], name="Solvent Out"))
        fig3.update_layout(barmode='group', title="Solvent In/Out per Batch")
        st.plotly_chart(fig3, use_container_width=True)

    # Utilities KPIs - Separate Graphs
    with st.container():
        st.subheader("Utilities KPIs")
        util = kpis["Utilities"]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Boiler Steam (kg)", f"{util['Boiler Steam (kg)']:.0f}")
        col2.metric("Chiller Energy (kWh)", f"{util['Chiller Energy (kWh)']:.0f}")
        col3.metric("HVAC Energy (kWh)", f"{util['HVAC Energy (kWh)']:.0f}")
        col4.metric("Vacuum Energy (kWh)", f"{util['Vacuum Energy (kWh)']:.0f}")

        st.caption("Boiler Steam per Batch")
        fig_boiler = px.bar(data, x="BatchID", y="Boiler_Steam_kg", title="Boiler Steam (kg) per Batch")
        st.plotly_chart(fig_boiler, use_container_width=True)

        st.caption("Chiller Energy per Batch")
        fig_chiller = px.bar(data, x="BatchID", y="Chiller_Energy_kWh", title="Chiller Energy (kWh) per Batch")
        st.plotly_chart(fig_chiller, use_container_width=True)

        st.caption("HVAC Energy per Batch")
        fig_hvac = px.bar(data, x="BatchID", y="HVAC_Energy_kWh", title="HVAC Energy (kWh) per Batch")
        st.plotly_chart(fig_hvac, use_container_width=True)

        st.caption("Vacuum Energy per Batch")
        fig_vacuum = px.bar(data, x="BatchID", y="Vacuum_Energy_kWh", title="Vacuum Energy (kWh) per Batch")
        st.plotly_chart(fig_vacuum, use_container_width=True)

    # Yield & Energy per kg API
    with st.container():
        st.subheader("Yield & Energy per kg API")
        col1, col2 = st.columns(2)
        col1.caption("Crystallizer Yield per Batch")
        fig5 = px.line(data, x="BatchID", y="Crystallizer_Yield", color="Product", title="Crystallizer Yield (%)")
        col1.plotly_chart(fig5, use_container_width=True)
        col2.caption("Energy Use per kg API")
        energy_per_kg = (data["Dryer_Energy_kWh"] + data["Distillation_Energy_kWh"] +
                         data["Chiller_Energy_kWh"] + data["HVAC_Energy_kWh"] +
                         data["Vacuum_Energy_kWh"]) / data["Batch_Throughput_kg"]
        fig6 = px.bar(
            x=data["BatchID"], y=energy_per_kg,
            labels={"x": "BatchID", "y": "Energy (kWh/kg)"},
            title="Total Energy Use per kg API")
        col2.plotly_chart(fig6, use_container_width=True)
