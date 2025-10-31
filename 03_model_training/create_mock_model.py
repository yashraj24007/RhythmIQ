#!/usr/bin/env python3
"""
Quick Model Generator - Creates a mock model for testing
"""

import os
import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np

print("🫀 Creating mock model for testing...")

# Create a simple RandomForest model
model = RandomForestClassifier(n_estimators=10, random_state=42)

# Create some dummy data to train it (required for the model to work)
X_dummy = np.random.rand(100, 128*128*3)  # 100 samples, 128x128x3 flattened
y_dummy = np.random.randint(0, 6, 100)  # 6 classes

# Train the model
print("📊 Training mock model...")
model.fit(X_dummy, y_dummy)

# Define class names
class_names = ['F', 'M', 'N', 'Q', 'S', 'V']

# Save model
model_data = {
    'model': model,
    'class_names': class_names
}

# Create directory if it doesn't exist
os.makedirs('05_trained_models', exist_ok=True)

# Save model
model_path = '05_trained_models/rythmguard_model.joblib'
joblib.dump(model_data, model_path)

print(f"✅ Model saved to: {model_path}")
print(f"🎯 Classes: {class_names}")
print("\n⚠️  Note: This is a MOCK model for testing only!")
print("   For production, train with real ECG data using simple_train.py")
