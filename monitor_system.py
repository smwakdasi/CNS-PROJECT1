import pandas as pd
import joblib
import psutil
import time
import os
import signal
import random
from plyer import notification

# Step 1: Load the trained model
model = joblib.load('ransomware_model.pkl')
print("✅ Model loaded...")

while True:
    # Step 2: Gather real-time system stats
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    procs = len(psutil.pids())

    print("🖥️ System Snapshot:")
    print(f"CPU: {cpu}%, Memory: {mem}%, Processes: {procs}")

    # Step 3: Build model input
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

    # Step 4: Make prediction
    result = model.predict(sample_input)[0]
    verdict = "RANSOMWARE" if result == 0 else "Benign"

    # Step 5: Log result
    with open("logs.txt", "a") as log:
        log.write(f"{time.ctime()} - Prediction: {verdict}\n")

    # Step 6: Display result
    if result == 0:
        print("⚠️ RANSOMWARE DETECTED!\n")

        # Alert user
        notification.notify(
            title="🚨 Ransomware Alert",
            message="⚠️ Suspicious system activity detected!",
            timeout=5
        )

        # Kill notepad.exe (simulation target)
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

    # Step 7: Wait before next check
    time.sleep(10)
