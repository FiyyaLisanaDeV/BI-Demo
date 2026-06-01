import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="Complaints", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Complaint Dashboard")

df_comp = load_mart("mart_complaints")

if df_comp.empty:
    st.warning("Data not available.")
else:
    render_summary(df_comp, "complaints")
    col1, col2, col3 = st.columns(3)
    tot_comp = len(df_comp)
    open_comp = len(df_comp[df_comp['status'] == 'OPEN'])
    high_prio = len(df_comp[df_comp['priority'] == 'HIGH'])
    
    col1.metric("Total Komplain", f"{tot_comp:,}")
    col2.metric("Komplain Open", f"{open_comp:,}")
    col3.metric("High Priority", f"{high_prio:,}")
    
    st.markdown("---")
    st.subheader("Komplain per Kategori")
    fig = px.pie(df_comp, names='complaint_category')
    st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    st.subheader("Daftar Komplain Open")
    df_open = df_comp[df_comp['status'] == 'OPEN']
    st.dataframe(df_open)
    apply_download_button(df_open, "open_complaints.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan SLA Pengaduan:**
    - **Tingkat Penyelesaian (Resolution Rate):** `(Σ Pengaduan berstatus RESOLVED / Σ Total Pengaduan Masuk) × 100%`
    - Pengaduan yang belum *Resolved* dianggap sebagai tanggungan operasional (Outstanding Tickets) yang memengaruhi metrik kualitas layanan nasabah.
    """)
