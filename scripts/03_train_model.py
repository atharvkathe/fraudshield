import pandas as pd
import joblib
import os
from sklearn.ensemble import IsolationForest

# --- Configuration ---
INPUT_FILE = 'data/processed/processed_transactions.csv'
MODEL_OUTPUT_FILE = 'models/isolation_forest.joblib'

if __name__ == "__main__":
    print(f"Loading processed data from '{INPUT_FILE}'...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Processed data file not found at '{INPUT_FILE}'")
        print("Please run 'scripts/02_preprocess_data.py' first.")
        exit()
        
    df = pd.read_csv(INPUT_FILE)
    print("Processed data loaded successfully.")

    if 'is_fraud' in df.columns:
        X = df.drop('is_fraud', axis=1)
        y = df['is_fraud']
    else:
        X = df
        y = None

    print(f"\nTraining Isolation Forest model on {len(X.columns)} features...")

    model = IsolationForest(
        n_estimators=100,
        max_samples='auto',
        contamination=0.05,
        random_state=42
    )

    model.fit(X)
    print("Model training complete.")

    os.makedirs(os.path.dirname(MODEL_OUTPUT_FILE), exist_ok=True)
    
    joblib.dump(model, MODEL_OUTPUT_FILE)
    
    print(f"\n✅ Model saved successfully to '{MODEL_OUTPUT_FILE}'")

