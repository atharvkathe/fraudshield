import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_model, style_risk, simulate_alert, generate_demo_data

# --- Configuration ---
MODEL_PATH = 'models/isolation_forest.joblib'
# --- Smart Mapping Configuration ---
# Define synonyms for required columns to enable auto-detection
COLUMN_SYNONYMS = {
    'amount': ['amount', 'amt', 'price', 'cost', 'value'],
    'location': ['location', 'city', 'state', 'region', 'country', 'loc'],
    'merchant': ['merchant', 'store', 'vendor', 'retailer'],
    'channel': ['channel', 'method', 'type', 'source']
}

# --- Page Setup ---
st.set_page_config(page_title="FraudShield AI", page_icon="🛡️", layout="wide")

# --- Main App UI ---
st.title("🛡️ FraudShield AI Dashboard")
st.markdown("### Anomaly Detection for Financial Transactions")

# --- Load Model ---
model = load_model(MODEL_PATH)

# --- Helper function for Smart Column Detection ---
def find_best_match(column_list, synonyms):
    """Finds the best matching column from a list based on a list of synonyms."""
    for syn in synonyms:
        for col in column_list:
            if syn in col.lower():
                return col
    return None

# --- Full Analysis Pipeline Function ---
def run_full_analysis(df, mapping=None):
    """Takes a dataframe and runs the full preprocessing and prediction pipeline."""
    with st.spinner("⚙️ Processing and analyzing your data..."):
        df_analysis = df.copy()
        
        if mapping:
            if len(set(mapping.values())) != len(mapping.values()):
                st.error("Error: Duplicate columns selected. Please map each required field to a unique column.")
                return
            rename_dict = {v: k for k, v in mapping.items()}
            df_analysis.rename(columns=rename_dict, inplace=True)
        
        # --- Feature Engineering (must match training script) ---
        if 'timestamp' in df_analysis.columns:
            df_analysis['timestamp'] = pd.to_datetime(df_analysis['timestamp'], errors='coerce')
        else:
            df_analysis['timestamp'] = pd.Timestamp.now()
            
        df_analysis['hour_of_day'] = df_analysis['timestamp'].dt.hour
        df_analysis['day_of_week'] = df_analysis['timestamp'].dt.dayofweek
        
        categorical_features_to_encode = ['location', 'merchant', 'channel']
        df_processed = pd.get_dummies(df_analysis, columns=categorical_features_to_encode, prefix=categorical_features_to_encode)
        
        trained_features = model.feature_names_in_
        
        for col in trained_features:
            if col not in df_processed.columns:
                df_processed[col] = 0
        df_processed = df_processed[trained_features]

        anomaly_scores = model.decision_function(df_processed)
        df_analysis['risk_score'] = -1 * anomaly_scores
        
        st.session_state.results = df_analysis.sort_values(by='risk_score', ascending=False)

# --- Sidebar for Data Input ---
with st.sidebar:
    st.header("1. Choose Data Source")
    source_choice = st.radio(
        "How do you want to provide data?",
        ("Use Demo Data", "Upload My Own CSV"),
        horizontal=True, label_visibility="collapsed"
    )

    if source_choice == "Use Demo Data":
        if st.button("Generate & Analyze Demo Data", type="primary"):
            demo_df = generate_demo_data()
            st.session_state.df_upload = demo_df
            run_full_analysis(demo_df)

    else: # User chose to upload
        uploaded_file = st.file_uploader("Upload your transaction CSV", type="csv")
        if uploaded_file:
            df_upload = pd.read_csv(uploaded_file)
            st.session_state.df_upload = df_upload
            
            st.header("2. Confirm Columns")
            st.info("I've tried to auto-detect your columns. Please confirm they are correct.")
            
            column_mapping = {}
            all_cols = df_upload.columns.tolist()
            
            for req_col, synonyms in COLUMN_SYNONYMS.items():
                best_guess = find_best_match(all_cols, synonyms)
                # Find the index of the best guess to set the selectbox default
                try:
                    default_index = all_cols.index(best_guess) if best_guess else 0
                except ValueError:
                    default_index = 0
                    
                column_mapping[req_col] = st.selectbox(
                    f"'{req_col.capitalize()}' column:",
                    options=all_cols, index=default_index,
                    help=f"Select the column representing: {synonyms}"
                )
            
            is_mapping_valid = len(set(column_mapping.values())) == len(column_mapping)
            if not is_mapping_valid:
                st.error("Duplicate columns selected. Each field must be unique.")

            if st.button("Confirm & Analyze", type="primary", disabled=not is_mapping_valid):
                run_full_analysis(st.session_state.df_upload, column_mapping)

# --- Main Content Area for Results ---
if 'results' in st.session_state:
    st.success("Analysis Complete!")
    results_df = st.session_state.results

    with st.expander("Show Analyzed Data with Risk Scores"):
        st.dataframe(results_df)

    st.subheader("Dashboard Summary")
    dynamic_threshold = results_df['risk_score'].quantile(0.95)
    num_flagged = (results_df['risk_score'] >= dynamic_threshold).sum()
    percentage_flagged = (num_flagged / len(results_df)) * 100 if len(results_df) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions Analyzed", f"{len(results_df):,}")
    col2.metric("High-Risk Transactions (Top 5%)", f"{num_flagged:,}", f"{percentage_flagged:.2f}%")
    col3.metric("Highest Risk Score", f"{results_df['risk_score'].max():.4f}")

    st.subheader("Top Flagged Transactions")
    st.dataframe(results_df[results_df['risk_score'] >= dynamic_threshold].head(20).style.map(style_risk, subset=['risk_score']))

    st.subheader("Visual Analysis")
    fig_hist = px.histogram(
        results_df, x='risk_score', nbins=100,
        title='Distribution of Transaction Risk Scores'
    )
    fig_hist.add_vline(x=dynamic_threshold, line_width=3, line_dash="dash", line_color="red", annotation_text="Top 5% Threshold")
    st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.info("Choose a data source and start the analysis from the sidebar.")
