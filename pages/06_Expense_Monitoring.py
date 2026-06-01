import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="Expense Monitoring", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Expense Monitoring")

df_exp = load_mart("mart_expense")

if df_exp.empty:
    st.warning("Data not available.")
else:
    render_summary(df_exp, "expense")
    col1, col2, col3 = st.columns(3)
    tot_exp = df_exp['amount'].sum()
    tot_trx = len(df_exp)
    pend_app = len(df_exp[df_exp['approval_status'] == 'PENDING'])
    
    col1.metric("Total Biaya", f"Rp {tot_exp:,.2f}")
    col2.metric("Jumlah Transaksi", f"{tot_trx:,}")
    col3.metric("Approval Pending", f"{pend_app:,}")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Biaya per Kategori")
        fig1 = px.bar(df_exp.groupby('expense_category')['amount'].sum().reset_index(), x='expense_category', y='amount')
        st.plotly_chart(fig1, width='stretch')
    with c2:
        st.subheader("Biaya per Unit")
        fig2 = px.pie(df_exp, names='department', values='amount')
        st.plotly_chart(fig2, width='stretch')
        
    st.markdown("---")
    st.subheader("Detail Biaya")
    st.dataframe(df_exp.head(100))
    apply_download_button(df_exp, "expense_data.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan Biaya Operasional (Opex):**
    - **Total Expense:** Agregasi riil dari jurnal pengeluaran (ledger pengeluaran biaya).
    - Seluruh perhitungan nominal belum termasuk depresiasi aset penyusutan, murni arus kas keluar (Cash-basis Opex) untuk kegiatan operasional bank sehari-hari.
    """)
