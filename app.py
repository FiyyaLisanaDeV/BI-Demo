import streamlit as st
from src.loader import check_data_availability

st.set_page_config(
    page_title="Finance BI BPR Simulasi BPR",
    page_icon="📊",
    layout="wide"
)

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Finance BI BPR Simulasi BPR")

st.markdown("""
### Selamat Datang di Dashboard Simulasi Finance BI
Aplikasi ini merupakan **Dashboard Simulasi** untuk pengolahan data Business Intelligence (BI) pada BPR.

**Penting:**
- Data yang ditampilkan adalah **Data Dummy** yang digenerate oleh sistem.
- Tidak ada data pribadi asli/nasabah riil yang digunakan.
- Sistem ini digunakan untuk tujuan simulasi arsitektur data mentah menjadi data siap analisis.

Gunakan menu di sidebar (sebelah kiri) untuk menavigasi ke berbagai modul dashboard.
""")

if not check_data_availability():
    st.error("⚠️ Data Mart belum tersedia. Silakan jalankan script transformasi data (transform_to_mart.py) terlebih dahulu melalui terminal.")
else:
    st.success("✅ Sistem berjalan normal. Data siap digunakan.")
    
st.info("💡 **Tips:** Anda dapat mendownload hasil filter di masing-masing halaman dashboard menggunakan tombol Download CSV.")
