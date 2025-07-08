import pandas as pd
import joblib
import psutil
import time
import os
import signal
import random
from plyer import notification

# Load trained model
model = joblib.load('ransomware_model.pkl')
print("✅ Model loaded...")

# Toggle this to simulate ransomware behavior
simulate_ransomware = False  # Set to True if you want to simulate detection

while True:
    # Get system stats (real or simulated)
    if simulate_ransomware:
        cpu = 97
        mem = 93
        procs = 350
    else:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        procs = len(psutil.pids())

    print(f"🖥️ CPU: {cpu}%, Memory: {mem}%, Processes: {procs}")

    # Format data as model input
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

    print("📦 Input to model:")
    print(sample_input)

    # Make prediction
    result = model.predict(sample_input)[0]
    label = "RANSOMWARE DETECTED" if result == 0 else "Benign"

    # Log prediction
    with open("logs.txt", "a", encoding="utf-8") as log:
        log.write(f"{time.ctime()} - Prediction: {label}\n")

    # Output and actions
    if result == 0:
        print("⚠️ RANSOMWARE DETECTED!\n")
        notification.notify(
            title="🚨 Ransomware Alert",
            message="⚠️ Suspicious system activity detected!",
            timeout=5
        )

        # Attempt to kill suspicious process (e.g., notepad.exe)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'notepad' in proc.info['name'].lower():
                    os.kill(proc.info['pid'], signal.SIGTERM)
                    print(f"🛑 Killed: {proc.info['name']} (PID {proc.info['pid']})")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    else:
        print("✅ System is behaving normally.\n")

    time.sleep(10)
