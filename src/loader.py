import pandas as pd
import streamlit as st
import os

MART_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'mart')

@st.cache_data
def load_mart(mart_name: str) -> pd.DataFrame:
    """Load data mart from CSV into pandas DataFrame"""
    file_path = os.path.join(MART_DIR, f"{mart_name}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

@st.cache_data
def check_data_availability() -> bool:
    """Check if data marts have been generated"""
    return os.path.exists(os.path.join(MART_DIR, 'mart_executive_summary.csv'))
