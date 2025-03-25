import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

# Generate synthetic transaction data (replace with real dataset)
np.random.seed(42)
transaction_data = pd.DataFrame({
    'Amount': np.concatenate([
        np.random.normal(50, 15, 490),  # Normal transactions
        np.random.normal(300, 50, 10)   # Fraudulent transactions
    ])
})

# Train Isolation Forest for fraud detection
model = IsolationForest(contamination=0.02, random_state=42)
model.fit(transaction_data[['Amount']])

# Save the trained model
joblib.dump(model, "models/fraud_detection.pkl")
print("✅ Fraud detection model saved as 'fraud_detection.pkl'")
