import streamlit as st
import plotly.express as px
import pandas as pd
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="Executive Summary", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Executive Summary")

df_snap = load_mart("mart_executive_summary")

if df_snap.empty:
    st.warning("Data not available.")
else:
    # Get latest snapshot
    df_snap['snapshot_date'] = pd.to_datetime(df_snap['snapshot_date'])
    latest = df_snap.sort_values('snapshot_date', ascending=False).iloc[0]
    
    render_summary(df_snap, "executive")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Nasabah", f"{latest['total_customers']:,}")
    col2.metric("Total DPK (Rp)", f"{latest['total_savings_balance'] + latest['total_deposit_balance']:,.2f}")
    col3.metric("Total Kredit (Rp)", f"{latest['total_loan_outstanding']:,.2f}")
    
    col4, col5, col6 = st.columns(3)
    col4.metric("NPL Ratio", f"{latest['npl_ratio']*100:.2f}%")
    col5.metric("Laba/Rugi Sblm Pajak", f"Rp {latest['profit_loss_before_tax']:,.2f}")
    col6.metric("Cash In (Rp)", f"{latest['cash_in']:,.2f}")
    
    st.markdown("---")
    st.subheader("Trend DPK & Kredit Bulanan")
    fig1 = px.line(df_snap, x='snapshot_date', y=['total_savings_balance', 'total_deposit_balance', 'total_loan_outstanding'], title="Trend DPK dan Kredit")
    st.plotly_chart(fig1, width='stretch')
    
    st.subheader("Trend NPL Bulanan")
    fig2 = px.line(df_snap, x='snapshot_date', y='npl_ratio', title="Trend NPL Ratio")
    st.plotly_chart(fig2, width='stretch')
    
    st.markdown("---")
    apply_download_button(df_snap, "executive_summary.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan Executive Summary:**
    - **Total DPK:** `Σ Saldo Akhir Tabungan + Σ Saldo Akhir Deposito`
    - **Total Kredit:** `Σ Baki Debet (Outstanding Principal)` seluruh fasilitas kredit aktif.
    - **Rasio NPL (Non-Performing Loan):** `(Σ Baki Debet Pinjaman NPL / Σ Total Baki Debet) × 100%`
    - **Laba/Rugi Sebelum Pajak:** `Σ Pendapatan Bunga & Operasional - Σ Biaya Operasional`
    """)
