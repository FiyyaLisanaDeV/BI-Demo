import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="NPL & Collection", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("NPL & Collection Dashboard")

df_npl = load_mart("mart_npl")

if df_npl.empty:
    st.warning("Data not available.")
else:
    df_filtered = df_npl.copy()
    
    render_summary(df_npl, "npl")
    col1, col2, col3 = st.columns(3)
    tot_out = df_filtered['outstanding_principal'].sum()
    npl_out = df_filtered[df_filtered['is_npl'] == True]['outstanding_principal'].sum()
    npl_ratio = (npl_out / tot_out) * 100 if tot_out > 0 else 0
    
    col1.metric("Total Outstanding", f"Rp {tot_out:,.2f}")
    col2.metric("NPL Nominal", f"Rp {npl_out:,.2f}")
    col3.metric("NPL Ratio", f"{npl_ratio:.2f}%")
    
    st.markdown("---")
    st.subheader("Sebaran Kolektibilitas")
    fig = px.pie(df_filtered, names='collectability_status', values='outstanding_principal', title="Outstanding Berdasarkan Kolektibilitas")
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    st.subheader("Daftar Fasilitas NPL")
    df_npl_only = df_filtered[df_filtered['is_npl'] == True]
    st.dataframe(df_npl_only.head(100))
    apply_download_button(df_npl_only, "npl_data.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan Kualitas Aktiva (NPL):**
    - **Definisi NPL:** Fasilitas kredit dengan status kolektibilitas: *Kurang Lancar* (DPD 91-120 hari), *Diragukan* (DPD 121-180 hari), atau *Macet* (>180 hari).
    - **Rasio NPL:** `(Σ Baki Debet Status NPL / Σ Total Baki Debet Keseluruhan) × 100%`
    - Sesuai standar Otoritas Jasa Keuangan (OJK), rasio NPL netto perbankan yang sehat harus dijaga di bawah 5%.
    """)
