import pandas as pd
import random
from faker import Faker
from datetime import datetime

# --- Configuration ---
OUTPUT_FILE = 'data/raw/transactions.csv'
NUM_TRANSACTIONS = 500

def generate_transaction_row(transaction_id):
    """Generates a single row of synthetic transaction data."""
    fake = Faker()
    
    user_id = f"U{random.randint(1, 100):03d}"
    amount = round(random.uniform(10, 20000), 2)
    timestamp = fake.date_time_between(start_date='-90d', end_date='now')
    city = fake.city()
    merchant = random.choice(['Amazon', 'Flipkart', 'Swiggy', 'Zomato', 'Paytm Mall', 'BigBazaar', 'Myntra', 'Snapdeal'])
    channel = random.choice(['Online', 'POS'])

    is_fraud = 0
    if amount > 15000:
        is_fraud = 1
    elif channel == 'Online' and city in ['Chennai', 'Gurgaon'] and random.random() > 0.9:
        is_fraud = 1

    return {
        "transaction_id": f"T{transaction_id:04d}",
        "timestamp": timestamp,
        "user_id": user_id,
        "amount": amount,
        "location": city,
        "merchant": merchant,
        "channel": channel,
        "is_fraud": is_fraud
    }

if __name__ == "__main__":
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    
    Faker.seed(42)
    random.seed(42)

    data = [generate_transaction_row(i) for i in range(1, NUM_TRANSACTIONS + 1)]
    df = pd.DataFrame(data)

    # Sort by time for realism
    df.sort_values(by="timestamp", inplace=True)

    # Save to CSV in the designated 'raw' data folder
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"✅ CSV generated successfully: {OUTPUT_FILE}")
    print("\n--- Data Preview ---")
    print(df.head())
    print("\n--- Fraud Counts ---")
    print(df['is_fraud'].value_counts())

