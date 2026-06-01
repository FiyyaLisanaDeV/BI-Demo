import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="Customer KYC", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Customer & KYC Dashboard")

df_cust = load_mart("mart_customer_kyc")

if df_cust.empty:
    st.warning("Data not available.")
else:
    render_summary(df_cust, "kyc")
    col1, col2, col3, col4 = st.columns(4)
    tot_cust = len(df_cust)
    act_cust = len(df_cust[df_cust['is_active'] == True])
    kyc_inc = len(df_cust[df_cust['kyc_status'] == 'INCOMPLETE'])
    high_risk = len(df_cust[df_cust['risk_profile'] == 'HIGH'])
    
    col1.metric("Total Nasabah", f"{tot_cust:,}")
    col2.metric("Nasabah Aktif", f"{act_cust:,}")
    col3.metric("KYC Incomplete", f"{kyc_inc:,}")
    col4.metric("High Risk", f"{high_risk:,}")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Sebaran Profil Risiko")
        fig1 = px.pie(df_cust, names='risk_profile')
        st.plotly_chart(fig1, width='stretch')
    with c2:
        st.subheader("Sektor Usaha")
        fig2 = px.bar(df_cust['business_sector'].value_counts().reset_index(), x='business_sector', y='count')
        st.plotly_chart(fig2, width='stretch')
        
    st.markdown("---")
    st.subheader("Data Nasabah (High Risk / Incomplete)")
    df_review = df_cust[(df_cust['kyc_status'] != 'COMPLETE') | (df_cust['risk_profile'] == 'HIGH')]
    st.dataframe(df_review.head(100))
    apply_download_button(df_review, "customer_kyc_data.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Penetapan Profil KYC (Know Your Customer):**
    - **Risk Profile (Profil Risiko):** Ditentukan oleh algoritma internal berdasarkan pekerjaan (contoh: PEP/Politically Exposed Person), sektor usaha, dan volume mutasi historis.
    - **Status KYC Incomplete:** Rekening dengan field mandatory yang belum terisi (misalnya: masa berlaku KTP habis atau nama ibu kandung kosong).
    """)
