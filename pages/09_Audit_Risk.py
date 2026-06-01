import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="Audit Risk", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Audit & Risk Dashboard")

df_audit = load_mart("mart_audit")

if df_audit.empty:
    st.warning("Data not available.")
else:
    render_summary(df_audit, "audit")
    col1, col2, col3 = st.columns(3)
    tot_evt = len(df_audit)
    high_risk = len(df_audit[df_audit['risk_flag'] == 'HIGH_RISK'])
    export_act = len(df_audit[df_audit['action_type'] == 'EXPORT'])
    
    col1.metric("Total Event", f"{tot_evt:,}")
    col2.metric("High Risk Event", f"{high_risk:,}")
    col3.metric("Aksi Export", f"{export_act:,}")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Event by Module")
        fig1 = px.pie(df_audit, names='module_name')
        st.plotly_chart(fig1, width='stretch')
    with c2:
        st.subheader("Event by Action Type")
        fig2 = px.bar(df_audit['action_type'].value_counts().reset_index(), x='action_type', y='count')
        st.plotly_chart(fig2, width='stretch')
        
    st.markdown("---")
    st.subheader("High Risk Activities")
    df_high = df_audit[df_audit['risk_flag'] == 'HIGH_RISK']
    st.dataframe(df_high.head(100))
    apply_download_button(df_high, "high_risk_audit.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Deteksi Risiko Audit (Audit Trail):**
    - **Severity High (Tingkat Keparahan Tinggi):** Dipicu oleh anomali seperti: akses *login* di luar jam kerja bank, perubahan data (UPDATE/DELETE) pada *core banking*, atau modifikasi profil tingkat otorisasi.
    - Seluruh pencatatan waktu (*timestamp*) menggunakan standar zona waktu UTC/WITA yang tersinkronisasi.
    """)
