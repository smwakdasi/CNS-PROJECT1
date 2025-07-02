import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

print("✅ Script is running...")

# Load Dataset
df = pd.read_csv('data/data_file.csv')  # Change path if needed
print("✅ Dataset loaded")

# Drop unnecessary columns
df = df.drop(['FileName', 'md5Hash'], axis=1)

# Separate features and label
X = df.drop('Benign', axis=1)
y = df['Benign']
print("✅ Features and labels separated")

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
print("✅ Data split into train and test sets")

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
print("✅ Training started...")
model.fit(X_train, y_train)
print("✅ Training completed")

# Evaluate
y_pred = model.predict(X_test)
print("✅ Evaluation results:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'ransomware_model.pkl')
print("✅ Model saved as ransomware_model.pkl")

# Plot feature importance (TEMPORARILY DISABLED)
# plt.figure(figsize=(10, 6))
# sns.barplot(x=model.feature_importances_, y=X.columns)
# plt.title("Feature Importance")
# plt.tight_layout()
# plt.show()

print("✅ Script finished successfully.")
