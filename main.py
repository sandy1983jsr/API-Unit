import streamlit as st
from data_acquisition.upload import get_data
from models.reactor import ReactorTwin
from models.dryer import DryerTwin
from models.sru import SRUTwin
from models.utility import UtilityTwin
from processing.kpi import compute_kpis
from simulation.whatif import run_whatif
from visualization.dashboard import show_dashboard

st.set_page_config(page_title="Pharma API Digital Twin", layout="wide")
st.title("🧠 Pharma API Unit Digital Twin")

# Data input
st.sidebar.header("Data Input")
data_choice = st.sidebar.radio("Choose Data Source:", ["Random Sample Data", "Upload CSV"])

data = get_data(data_choice)
if data is None:
    st.warning("No data loaded. Please generate or upload data.")
    st.stop()

# Digital Twin Models
reactor = ReactorTwin(data)
dryer = DryerTwin(data)
sru = SRUTwin(data)
utility = UtilityTwin(data)

# KPIs
kpis = compute_kpis(reactor, dryer, sru, utility)

# Dashboard
show_dashboard(data, kpis)

# What-if
st.header("🧪 What-if Simulation")
run_whatif(data, reactor, dryer, sru, utility)
