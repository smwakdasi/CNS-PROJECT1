import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

print("✅ Script is running...")

# Load dataset
df = pd.read_csv('data/data_file.csv', low_memory=False)
print("✅ Dataset loaded")

# Drop unnecessary columns
df = df.drop(['FileName', 'md5Hash'], axis=1)

# Convert all columns to numeric (in case of type errors)
df = df.apply(pd.to_numeric, errors='coerce')
df = df.dropna()  # Drop rows with any missing values

# Separate features and target label
X = df.drop('Benign', axis=1)
y = df['Benign']
print("✅ Features and labels separated")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("✅ Data split into train and test sets")

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("✅ Training started...")
model.fit(X_train, y_train)
print("✅ Training completed")

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy:.2f}")
print("✅ Classification Report:")
report = classification_report(y_test, y_pred)
print(report)

# Optional: save report to file
with open("model_evaluation.txt", "w") as f:
    f.write("Classification Report:\n")
    f.write(report)
    f.write(f"\nAccuracy: {accuracy:.2f}")

# Save trained model
joblib.dump(model, 'ransomware_model.pkl')
print("✅ Model saved as ransomware_model.pkl")

print("✅ Script finished successfully.")
