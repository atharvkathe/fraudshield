import streamlit as st
import pandas as pd
import joblib
import os
from faker import Faker
import random

# --- Utility Functions ---

@st.cache_resource
def load_model(path):
    """Loads the pre-trained model from disk."""
    if not os.path.exists(path):
        st.error(f"Model file not found at '{path}'. Please run the training script first.")
        return None
    return joblib.load(path)

@st.cache_data
def generate_demo_data(num_rows=500):
    """Generates a DataFrame of synthetic transaction data for demo purposes."""
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    data = []
    for i in range(1, num_rows + 1):
        amount = round(random.uniform(10, 20000), 2)
        channel = random.choice(['Online', 'POS'])
        is_fraud = 1 if amount > 15000 else 0
        data.append({
            "transaction_id": f"T{i:04d}",
            "timestamp": fake.date_time_between(start_date='-90d', end_date='now'),
            "user_id": f"U{random.randint(1, 100):03d}",
            "amount": amount,
            "location": fake.city(),
            "merchant": random.choice(['Amazon', 'Flipkart', 'Swiggy', 'Zomato']),
            "channel": channel,
            "is_fraud": is_fraud # Include for potential accuracy checks
        })
    return pd.DataFrame(data)

def style_risk(score):
    """Applies a background color based on the risk score."""
    if score > 0.01: 
        return 'background-color: #ff4d4d; color: white'
    elif score > 0.005: 
        return 'background-color: #ff9999'
    return ''

def simulate_alert(transaction):
    """Displays a toast notification to simulate an alert."""
    st.toast(f"🚨 CRITICAL ALERT! High-risk transaction detected!", icon="🚨")

