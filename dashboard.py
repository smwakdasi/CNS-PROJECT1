import streamlit as st
import pandas as pd
import psutil
import joblib
import random
import time
from datetime import datetime

# Load model
model = joblib.load("ransomware_model.pkl")

# Streamlit UI Config
st.set_page_config(page_title="Ransomware Dashboard", layout="centered")
st.title("🛡️ Real-Time Ransomware Detection")
st.markdown("Built with love using Streamlit")

# Storage for metrics
cpu_history = []
mem_history = []
timestamps = []

# UI layout
col1, col2 = st.columns(2)
placeholder = st.empty()
log_viewer = st.expander("📄 View Detection Logs")

# --- Controls ---
simulate = st.checkbox("🔁 Demo Mode: Simulate Ransomware Spike")
max_cycles = st.number_input("🔢 Number of Detection Cycles", min_value=1, max_value=100, value=10, step=1)
run_toggle = st.checkbox("▶️ Run Detection")

# If detection is toggled on
if run_toggle:
    for i in range(int(max_cycles)):
        now = datetime.now().strftime("%H:%M:%S")

        # Use simulated or real values
        if simulate:
            cpu = 97
            mem = 93
            procs = 350
        else:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            procs = len(psutil.pids())

        # Append to history
        cpu_history.append(cpu)
        mem_history.append(mem)
        timestamps.append(now)

        # Sample input for model
        sample_input = pd.DataFrame([{
            "Machine": 332,
            "DebugSize": int(cpu),
            "DebugRVA": int(mem),
            "MajorImageVersion": 10,
            "MajorOSVersion": 10,
            "ExportRVA": procs,
            "ExportSize": random.randint(0, 1000),
            "IatVRA": 8192,
            "MajorLinkerVersion": 14,
            "MinorLinkerVersion": 10,
            "NumberOfSections": 6,
            "SizeOfStackReserve": 262144,
            "DllCharacteristics": 16736,
            "ResourceSize": 1024,
            "BitcoinAddresses": 0
        }])

        # Predict
        prediction = model.predict(sample_input)[0]
        label = "RANSOMWARE DETECTED!" if prediction == 0 else "Benign"

        # Log (UTF-8 + clean)
        clean_label = "RANSOMWARE DETECTED" if prediction == 0 else "Benign"
        with open("logs.txt", "a", encoding="utf-8") as log:
            log.write(f"{datetime.now()} - Prediction: {clean_label}\n")

        # Dashboard UI
        with placeholder.container():
            col1.metric("CPU Usage", f"{cpu}%")
            col1.metric("Memory Usage", f"{mem}%")
            col2.metric("Running Processes", procs)
            st.subheader("Model Prediction")
            st.success(label) if prediction == 1 else st.error(label)
            st.code(sample_input.to_string(index=False))

            st.line_chart(pd.DataFrame({
                "CPU (%)": cpu_history,
                "Memory (%)": mem_history
            }, index=timestamps))

        # Show log content
        with log_viewer:
            with open("logs.txt", "r", encoding="utf-8") as log:
                content = log.read()
                st.text_area("Log Output", content, height=200)

        time.sleep(5)

    st.success("✅ Detection cycle completed.")
