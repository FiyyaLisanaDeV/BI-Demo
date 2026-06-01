import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="DPK Dashboard", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("DPK Dashboard (Dana Pihak Ketiga)")

df_dpk = load_mart("mart_dpk")

if df_dpk.empty:
    st.warning("Data not available.")
else:
    # Filter
    products = df_dpk['product_name'].unique()
    selected_prod = st.sidebar.multiselect("Pilih Produk", products, default=products)
    
    df_filtered = df_dpk[df_dpk['product_name'].isin(selected_prod)]
    
    render_summary(df_filtered, "dpk")
    col1, col2, col3 = st.columns(3)
    tot_sav = df_filtered[df_filtered['account_type'] == 'SAVINGS']['balance'].sum()
    tot_dep = df_filtered[df_filtered['account_type'] == 'DEPOSIT']['balance'].sum()
    
    col1.metric("Total Tabungan", f"Rp {tot_sav:,.2f}")
    col2.metric("Total Deposito", f"Rp {tot_dep:,.2f}")
    col3.metric("Total DPK", f"Rp {tot_sav + tot_dep:,.2f}")
    
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Komposisi Produk DPK")
        fig1 = px.pie(df_filtered, names='product_name', values='balance', title="Saldo per Produk")
        st.plotly_chart(fig1, width='stretch')
        
    with col_chart2:
        st.subheader("Top Nasabah (Dummy)")
        top_cust = df_filtered.groupby(['customer_id', 'full_name'])['balance'].sum().reset_index().sort_values('balance', ascending=False).head(10)
        st.dataframe(top_cust)
        
    st.markdown("---")
    st.subheader("Daftar Rekening")
    st.dataframe(df_filtered.head(100))
    apply_download_button(df_filtered, "dpk_data.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan DPK (Dana Pihak Ketiga):**
    - **Saldo Tabungan:** Nilai buku riil (current balance) dari rekening simpanan nasabah.
    - **Saldo Deposito:** Nilai pokok penempatan (principal) deposito berjangka yang belum jatuh tempo.
    - **Total DPK:** `Σ Saldo Tabungan + Σ Saldo Deposito`. Tidak termasuk kewajiban antar bank.
    """)
