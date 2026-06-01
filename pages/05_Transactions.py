import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button
import pandas as pd

st.set_page_config(page_title="Transactions", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Teller & Transaction Dashboard")

df_trx = load_mart("mart_transactions")

if df_trx.empty:
    st.warning("Data not available.")
else:
    df_trx['date_only'] = pd.to_datetime(df_trx['date_only'])
    
    render_summary(df_trx, "transactions")
    col1, col2, col3, col4 = st.columns(4)
    tot_vol = len(df_trx)
    tot_val = df_trx['amount'].sum()
    cash_in = df_trx[(df_trx['transaction_status'] == 'SUCCESS') & (df_trx['debit_credit'] == 'CREDIT')]['amount'].sum()
    cash_out = df_trx[(df_trx['transaction_status'] == 'SUCCESS') & (df_trx['debit_credit'] == 'DEBIT')]['amount'].sum()
    
    col1.metric("Volume Transaksi", f"{tot_vol:,}")
    col2.metric("Nilai Transaksi", f"Rp {tot_val:,.2f}")
    col3.metric("Cash In", f"Rp {cash_in:,.2f}")
    col4.metric("Cash Out", f"Rp {cash_out:,.2f}")
    
    st.markdown("---")
    st.subheader("Trend Transaksi Harian")
    trend = df_trx.groupby('date_only')['amount'].sum().reset_index()
    fig = px.line(trend, x='date_only', y='amount', title="Trend Nilai Transaksi")
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    st.subheader("Data Transaksi Terakhir")
    st.dataframe(df_trx.sort_values('transaction_date', ascending=False).head(100))
    apply_download_button(df_trx, "transactions_data.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan Transaksi & Mutasi:**
    - **Volume Transaksi:** Total frekuensi (jumlah baris/tiket) mutasi yang berhasil (*SUCCESS*).
    - **Cash In (Uang Masuk):** `Σ Nominal Mutasi` dengan sandi transaksi Kredit (CR).
    - **Cash Out (Uang Keluar):** `Σ Nominal Mutasi` dengan sandi transaksi Debit (DB).
    """)
