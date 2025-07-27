import pandas as pd
import os

# --- Configuration ---
INPUT_FILE = 'data/raw/transactions.csv'
OUTPUT_FILE = 'data/processed/processed_transactions.csv'

if __name__ == "__main__":
    print(f"Loading raw data from '{INPUT_FILE}'...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found at '{INPUT_FILE}'")
        print("Please run 'scripts/01_generate_data.py' first.")
        exit()
        
    df = pd.read_csv(INPUT_FILE)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    print("Raw data loaded successfully.")

    print("\nStarting feature engineering...")
    
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    print("Created 'hour_of_day' and 'day_of_week' features.")

    print("Applying one-hot encoding to categorical features...")
    categorical_features = ['location', 'merchant', 'channel']
    df = pd.get_dummies(df, columns=categorical_features, prefix=categorical_features)
    print("Encoding complete.")

    columns_to_drop = ['transaction_id', 'timestamp', 'user_id']
    df_processed = df.drop(columns=columns_to_drop)
    print(f"Dropped unnecessary columns: {columns_to_drop}")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Save the processed data
    df_processed.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\n✅ Processed data saved successfully to '{OUTPUT_FILE}'")
    print("\n--- Processed Data Preview ---")
    print(df_processed.head())
    print(f"\nTotal features in processed data: {len(df_processed.columns)}")