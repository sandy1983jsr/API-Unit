import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import plotly.express as px

# A) Predictive indicators & preventive maintenance triggers
def predictive_maintenance(data):
    st.subheader("A) Predictive Indicators & Preventive Maintenance")
    # Example: Predict Dryer Energy anomaly as maintenance trigger
    model = IsolationForest(contamination=0.1)
    data['dry_energy_anom'] = model.fit_predict(data[['Dryer_Energy_kWh']])
    anom_batches = data[data['dry_energy_anom'] == -1]
    if not anom_batches.empty:
        st.warning("Trigger Preventive Maintenance for batches:")
        st.dataframe(anom_batches[['BatchID','Dryer_Energy_kWh']])
    else:
        st.success("No preventive maintenance trigger found.")

# B) Set tuning set points (Optimization)
def recommend_setpoints(data):
    st.subheader("B) Set Tuning Set Points (Optimization)")
    # Example: Find setpoints that minimize Dryer_Energy_kWh while maintaining Yield
    X = data[["Reactor_Temp", "Reactor_Agitation", "Reactor_Time"]]
    y = data["Dryer_Energy_kWh"]
    model = RandomForestRegressor().fit(X, y)
    idx = y.idxmin()
    best = X.loc[idx]
    st.info(f"Recommended set points for lowest dryer energy: Temp={best['Reactor_Temp']:.1f}, Agitation={best['Reactor_Agitation']:.0f}, Time={best['Reactor_Time']:.2f}")

# C) Recommend process parameter range for best yield/lowest emissions
def recommend_param_ranges(data):
    st.subheader("C) Recommend Parameter Ranges for Best Yield/Lowest Emissions")
    # Get top 20% batches by yield, show their parameter ranges
    top = data.nlargest(int(len(data)*0.2), 'Crystallizer_Yield')
    st.write("Parameter ranges for top 20% yield batches:")
    st.dataframe(top[["Reactor_Temp","Reactor_Agitation","Reactor_Time","Dryer_Time"]].describe().loc[["min","max"]])
    # Similarly, for lowest COD
    low_cod = data.nsmallest(int(len(data)*0.2), "ETP_COD_mgL")
    st.write("Parameter ranges for lowest emissions (COD):")
    st.dataframe(low_cod[["Reactor_Temp","Reactor_Agitation","Reactor_Time","Dryer_Time"]].describe().loc[["min","max"]])

# D) Pattern mining for best operating windows
def pattern_mining_windows(data):
    st.subheader("D) Pattern Mining for Best Historical Operating Windows")
    features = ["Reactor_Temp","Reactor_Agitation","Reactor_Time","Dryer_Time"]
    scaler = MinMaxScaler()
    X = scaler.fit_transform(data[features])
    kmeans = KMeans(n_clusters=3, random_state=42).fit(X)
    data['cluster'] = kmeans.labels_
    best_cluster = data.groupby('cluster')['Crystallizer_Yield'].mean().idxmax()
    window = data[data['cluster']==best_cluster][features]
    st.info(f"Best operating window (cluster {best_cluster}) parameter ranges:")
    st.dataframe(window.describe().loc[["min","max"]])

# E) Generate model insights (feature importance)
def model_insights(data):
    st.subheader("E) Model Insights (Feature Importance)")
    X = data[["Reactor_Temp", "Reactor_Agitation", "Reactor_Time", "Dryer_Time"]]
    y = data["Crystallizer_Yield"]
    model = RandomForestRegressor().fit(X, y)
    importances = model.feature_importances_
    fig = px.bar(x=X.columns, y=importances, labels={'x':'Parameter','y':'Importance'}, title="Feature Importance for Yield")
    st.plotly_chart(fig, use_container_width=True)

# F) Time-series ML for predictive maintenance
def time_series_predictive_maintenance(data):
    st.subheader("F) Time-Series ML for Predictive Maintenance")
    # Example: Simple rolling mean anomaly detection
    dryer_energy = data["Dryer_Energy_kWh"]
    rolling = dryer_energy.rolling(window=3, min_periods=1).mean()
    anomaly = dryer_energy > (rolling.mean() + 2 * rolling.std())
    st.line_chart(pd.DataFrame({"Dryer Energy": dryer_energy, "Rolling Mean": rolling}))
    if anomaly.any():
        st.warning("Predictive maintenance trigger: Dryer energy spike detected!")
    else:
        st.success("No maintenance trigger found in time series.")

# G) Deep learning diagnostics (stub)
def deep_learning_diagnostics(data):
    st.subheader("G) Deep Learning for Non-linear Diagnostics")
    st.info("This is a placeholder. For production, integrate Keras/Tensorflow/PyTorch models here.")
    # Example: show a dummy chart
    st.line_chart(data[["Reactor_Temp", "Dryer_Energy_kWh"]])
    st.caption("Train a deep neural net for anomaly detection or yield prediction.")

# H) Reinforcement learning for process optimization (stub)
def reinforcement_learning_optimization(data):
    st.subheader("H) Reinforcement Learning for Continuous Process Optimization")
    st.info("This is a placeholder. For production, integrate a RL agent (e.g., using Stable Baselines3).")
    st.caption("Use RL to continuously adjust setpoints to maximize yield/minimize energy.")

# Main UI to call above via buttons
def ai_tools_ui(data):
    st.header("🔬 Advanced AI/ML Tools")
    if st.button("A) Predictive Maintenance Trigger"):
        predictive_maintenance(data)
    if st.button("B) Recommend Set Points"):
        recommend_setpoints(data)
    if st.button("C) Recommend Parameter Ranges for Best Yield/Emissions"):
        recommend_param_ranges(data)
    if st.button("D) Pattern Mining for Best Operating Windows"):
        pattern_mining_windows(data)
    if st.button("E) Generate Model Insights"):
        model_insights(data)
    if st.button("F) Time-series Predictive Maintenance"):
        time_series_predictive_maintenance(data)
    if st.button("G) Deep Learning Diagnostics"):
        deep_learning_diagnostics(data)
    if st.button("H) Reinforcement Learning Optimization"):
        reinforcement_learning_optimization(data)
