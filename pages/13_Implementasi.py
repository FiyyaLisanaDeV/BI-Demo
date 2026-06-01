import streamlit as st
from src.utils import check_password

st.set_page_config(page_title="Panduan Implementasi", layout="wide", page_icon="🚀")

if not check_password():
    st.stop()

st.title("🚀 Panduan Adopsi & Integrasi Sistem BI")
st.markdown("""
Halaman ini menjabarkan *cetak biru* (blueprint) komprehensif mengenai bagaimana platform Business Intelligence (BI) ini dapat diadopsi dari skala prototipe/simulasi menjadi solusi *Enterprise* berskala penuh di lingkungan perbankan, dengan kepatuhan mutlak terhadap **Regulasi Otoritas Jasa Keuangan (POJK)**.
""")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Strategi Adopsi (Fase Transisi)")
    st.markdown("""
    Adopsi teknologi analitik baru di sektor perbankan membutuhkan pendekatan kehati-hatian (*Prudential Approach*).
    
    *   **Fase 1: Shadow Run (Paralel):** Sistem BI ini tidak langsung menggantikan sistem pelaporan (*MIS*) yang ada, melainkan berjalan berdampingan. Data dari *Core Banking* diekstrak secara berkala (misal: H+1) untuk membandingkan akurasi agregasi BI dengan laporan manual.
    *   **Fase 2: User Acceptance Testing (UAT) Sektoral:** Pemberian akses terbatas ke beberapa kepala divisi (Kepala Kredit, Kepala Dana) untuk menguji validitas *Dashboard* KPI dan *NPL*.
    *   **Fase 3: Full Rollout & Decommissioning:** Menjadikan BI ini sebagai *"Single Source of Truth"* utama dalam rapat ALCO (*Asset and Liability Committee*) dan menonaktifkan pembuatan laporan manual berbasis Excel.
    """)
    
    st.header("2. Arsitektur Integrasi Sistem")
    st.markdown("""
    Untuk mengalirkan data tanpa mengganggu performa transaksi nasabah (*Production Database*), integrasi dilakukan melalui:
    
    *   **Read-Only Replica / Data Warehouse:** Platform BI dilarang keras menembak langsung ke *Core Banking System (CBS)*. Data harus diekstrak (*ETL*) ke peladen replika atau *Data Warehouse* (menggunakan format Parquet/Kolumnar) pada tengah malam (*Batch Processing*).
    *   **Secure API Gateway:** Untuk kebutuhan data yang bersifat semi-*real-time* (seperti *Fraud Detection* atau *Transaction Monitoring*), integrasi menggunakan API internal bank yang dienkripsi via jalur VPN tertutup, bukan internet publik.
    """)

with col2:
    st.header("3. Memaksimalkan Fungsi (Optimalisasi)")
    st.markdown("""
    Platform ini tidak sekadar menjadi alat visualisasi visual, fungsinya dapat diekspansi menjadi alat bantu pengambil keputusan strategis:
    
    *   **Otomasi Pelaporan Regulator (OBOX / LBU):** Skrip *Data Engineering* di *backend* dapat disesuaikan agar mampu memuntahkan format `.txt` atau `.csv` baku yang siap diunggah ke portal pelaporan Bank Indonesia atau OJK, memangkas waktu kerja administratif dari hitungan minggu menjadi detik.
    *   **Predictive Analytics (Machine Learning):** Dengan tersedianya *Data Mart* terpusat (seperti di halaman Data Lineage), tim *Data Scientist* dapat memasang algoritma AI untuk memprediksi probabilitas nasabah kredit jatuh ke status Macet (NPL) berdasarkan pola transaksinya.
    *   **Automated Alerting System:** Mengintegrasikan sistem deteksi anomali (*Audit Risk*) dengan email internal atau WhatsApp perusahaan untuk memberitahu manajemen ketika ada transaksi bernilai fantastis di luar kebiasaan (AML/CTF).
    """)

st.markdown("---")

st.header("🛡️ Kepatuhan POJK & Standar Kerahasiaan Data (Data Privacy)")
st.info("Sistem ini didesain sejak awal (*Security by Design*) untuk mematuhi regulasi perbankan Indonesia yang ketat.")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("POJK No. 11/POJK.03/2022")
    st.markdown("**Penyelenggaraan Teknologi Informasi (PTI)**")
    st.markdown("""
    *   **Audit Trail Aktif:** Setiap tindakan klik, filter, atau unduh oleh pengguna (pegawai) direkam secara absolut di sistem, mencakup *Timestamp* dan *IP Address*, menjamin *non-repudiation* (tidak dapat disangkal).
    *   **Role-Based Access Control (RBAC):** Pejabat kredit hanya bisa melihat performa AO di wilayah cabangnya sendiri. Direktur Utama memiliki hak akses paripurna.
    """)

with c2:
    st.subheader("POJK No. 6/POJK.07/2022")
    st.markdown("**Perlindungan Konsumen & Data Pribadi (PDP)**")
    st.markdown("""
    *   **Data Masking (Dynamic & Hard Masking):** Identitas PII (*Personally Identifiable Information*) seperti Nama Nasabah, NIK, dan No. Telepon disensor (contoh: *0812***7890*) baik di tampilan *User Interface* dasbor maupun di level unduhan CSV (seperti yang telah diimplementasikan).
    *   **Prinsip Need-to-Know:** Data yang tidak relevan dengan metrik agregasi makro akan di-*drop* di tahap ETL.
    """)

with c3:
    st.subheader("Ketahanan Siber (Cyber Resilience)")
    st.markdown("**Enkripsi & Arsitektur Terisolasi**")
    st.markdown("""
    *   **Data in Transit (HTTPS/TLS):** Semua transmisi visualisasi dari *server* ke *browser* pengguna diamankan dengan SSL/TLS 1.3.
    *   **Data at Rest (AES-256):** Berkas *Data Mart* (Parquet/CSV) yang tersimpan di ruang penyimpanan peladen dienkripsi secara fisik.
    *   Sistem ini tidak memfasilitasi antarmuka pengubahan data operasional secara langsung (*Write-Back*), menutup celah manipulasi angka kredit dari dalam dasbor.
    """)
