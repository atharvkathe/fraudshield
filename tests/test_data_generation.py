import pytest
import pandas as pd
import os
from scripts.o1_generate_data import generate_transaction_row, NUM_TRANSACTIONS

# --- Test Fixture ---
# A fixture is a function that runs before each test function to set up a baseline state.
@pytest.fixture(scope="module")
def generated_df():
    """
    Generates a DataFrame for testing and returns it.
    'scope="module"' means this will only run once for all tests in this file.
    """
    print("\n(Setting up test data...)")
    data = [generate_transaction_row(i) for i in range(1, NUM_TRANSACTIONS + 1)]
    df = pd.DataFrame(data)
    return df

# --- Test Functions ---
# Each test function must start with the word 'test_'.

def test_dataframe_creation(generated_df):
    """
    Test 1: Does the data generation produce a non-empty DataFrame?
    """
    assert generated_df is not None, "DataFrame should not be None"
    assert not generated_df.empty, "DataFrame should not be empty"
    print("✅ Test 1 Passed: DataFrame created successfully.")

def test_number_of_records(generated_df):
    """
    Test 2: Does the DataFrame have the correct number of rows?
    """
    assert len(generated_df) == NUM_TRANSACTIONS, f"Expected {NUM_TRANSACTIONS} rows, but got {len(generated_df)}"
    print(f"✅ Test 2 Passed: DataFrame has {NUM_TRANSACTIONS} records as expected.")

def test_expected_columns_exist(generated_df):
    """
    Test 3: Does the DataFrame contain all the columns we expect?
    """
    expected_cols = [
        "transaction_id", "timestamp", "user_id", "amount",
        "location", "merchant", "channel", "is_fraud"
    ]
    # Check if all expected columns are present in the DataFrame's columns
    assert all(col in generated_df.columns for col in expected_cols), "One or more expected columns are missing"
    print("✅ Test 3 Passed: All expected columns are present.")

def test_data_types(generated_df):
    """
    Test 4: Are the key columns of the correct data type?
    """
    assert pd.api.types.is_numeric_dtype(generated_df['amount']), "'amount' column should be numeric"
    assert pd.api.types.is_object_dtype(generated_df['transaction_id']), "'transaction_id' column should be a string/object"
    assert pd.api.types.is_integer_dtype(generated_df['is_fraud']), "'is_fraud' column should be an integer"
    print("✅ Test 4 Passed: Key columns have the correct data types.")

def test_fraud_flag_values(generated_df):
    """
    Test 5: Does the 'is_fraud' column only contain 0 or 1?
    """
    # The set of unique values in the column should be a subset of {0, 1}
    assert set(generated_df['is_fraud'].unique()).issubset({0, 1}), "'is_fraud' column contains invalid values"
    print("✅ Test 5 Passed: 'is_fraud' column contains only 0s and 1s.")

