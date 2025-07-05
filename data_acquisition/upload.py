import streamlit as st
import pandas as pd
import numpy as np

def random_sample_data(n_batches=20):
    np.random.seed(42)
    data = pd.DataFrame({
        "BatchID": np.arange(1, n_batches+1),
        "Reactor_Temp": np.random.uniform(70, 120, n_batches),
        "Reactor_Agitation": np.random.uniform(100, 300, n_batches),
        "Reactor_Time": np.random.uniform(3, 8, n_batches),
        "Dryer_Time": np.random.uniform(2, 6, n_batches),
        "Dryer_Energy_kWh": np.random.uniform(50, 200, n_batches),
        "Distillation_Energy_kWh": np.random.uniform(60, 250, n_batches),
        "Crystallizer_Yield": np.random.uniform(85, 99, n_batches),
        "Centrifuge_Loss_kg": np.random.uniform(0.1, 2.0, n_batches),
        "SRU_Solvent_In_kg": np.random.uniform(100, 500, n_batches),
        "SRU_Solvent_Out_kg": np.random.uniform(70, 490, n_batches),
        "ETP_COD_mgL": np.random.uniform(100, 300, n_batches),
        "ZLD_Water_Reused_m3": np.random.uniform(5, 25, n_batches),
        "Boiler_Steam_kg": np.random.uniform(200, 1200, n_batches),
        "Chiller_Energy_kWh": np.random.uniform(30, 180, n_batches),
        "HVAC_Energy_kWh": np.random.uniform(40, 160, n_batches),
        "Vacuum_Energy_kWh": np.random.uniform(10, 60, n_batches),
        "Batch_Throughput_kg": np.random.uniform(80, 120, n_batches),
        "Product": np.random.choice(["API-A", "API-B"], n_batches)
    })
    return data

def get_data(choice):
    if choice == "Random Sample Data":
        return random_sample_data()
    else:
        uploaded = st.sidebar.file_uploader("Upload CSV file", type="csv")
        if uploaded:
            try:
                data = pd.read_csv(uploaded)
                return data
            except Exception as e:
                st.error(f"Failed to read CSV: {e}")
        return None
