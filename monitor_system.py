import pandas as pd
import joblib
import psutil
import time

# Step 1: Load the trained model
model = joblib.load('ransomware_model.pkl')
print("✅ Model loaded...")

# Optional loop to simulate real-time monitoring (e.g., every 10 seconds)
while True:
    # Step 2: Gather real-time CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"🖥️ CPU Usage: {cpu_usage}%")

    # Step 3: Simulate system behavior input
    sample_input = pd.DataFrame([{
        "Machine": 332,
        "DebugSize": 0,
        "DebugRVA": 0,
        "MajorImageVersion": 10,
        "MajorOSVersion": 10,
        "ExportRVA": 0,
        "ExportSize": 0,
        "IatVRA": 8192,
        "MajorLinkerVersion": 14,
        "MinorLinkerVersion": 10,
        "NumberOfSections": 6,
        "SizeOfStackReserve": 262144,
        "DllCharacteristics": 16736,
        "ResourceSize": 1024,
        "BitcoinAddresses": 0
    }])

    # Step 4: Predict
    result = model.predict(sample_input)[0]

    # Step 5: Show result
    if result == 0:
        print("⚠️ RANSOMWARE DETECTED!\n")
    else:
        print("✅ System is behaving normally.\n")

    # Step 6: Wait 10 seconds before repeating
    time.sleep(10)
