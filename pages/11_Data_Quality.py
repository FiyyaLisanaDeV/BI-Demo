import streamlit as st
import pandas as pd
import os
from src.utils import apply_download_button

st.set_page_config(page_title="Data Quality", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Data Quality Dashboard")

report_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'rejected', 'validation_report.xlsx')

if not os.path.exists(report_path):
    st.warning("Validation report belum tersedia. Jalankan script validate_data.py terlebih dahulu.")
else:
    df_report = pd.read_excel(report_path)
    
    fails = df_report[df_report['status'] == 'FAIL']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Checks", len(df_report))
    col2.metric("Passed", len(df_report) - len(fails))
    col3.metric("Failed", len(fails), delta_color="inverse" if len(fails) > 0 else "off")
    
    st.markdown("---")
    if not fails.empty:
        st.error(f"Ditemukan {len(fails)} error pada data mentah!")
        st.dataframe(fails)
        apply_download_button(fails, "validation_fails.csv", "Download Log Error")
    else:
        st.success("Kualitas data sangat baik. Tidak ditemukan error.")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Validasi Kualitas Data:**
    - **Passing Rate (Persentase Lolos Uji):** `(Σ Baris Data Valid / Σ Baris Data Mentah) × 100%`.
    - Parameter Validasi mencakup: integritas numerik (tidak boleh negatif pada saldo), referensi silang (ID Nasabah di tabel kredit wajib ada di tabel utama), dan kelengkapan nilai (*Null-check*).
    """)
