<div align="center">

# 📊 Finance BI for BPR (Bank Perekonomian Rakyat)
**Enterprise-Grade Business Intelligence & Data Analytics Simulation**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*Proyek ini adalah Dashboard Business Intelligence interaktif berbasis Python & Streamlit yang dirancang khusus untuk mensimulasikan alur pengolahan dan visualisasi data perbankan (BPR).*

---

</div>

> ⚠️ **DISCLAIMER PENTING**  
> Seluruh data yang terdapat dalam repository ini adalah **DATA DUMMY** yang di-generate menggunakan sistem (library Faker). **TIDAK ADA data pribadi asli, NIK, atau data rahasia nasabah sungguhan** di dalam sistem ini.

<br>

## 🌟 Fitur Utama (Modules)
Sistem ini menyediakan 11 modul dashboard komprehensif yang membedah berbagai metrik perbankan:

- 📈 **Executive Summary:** Ringkasan tingkat tinggi performa bank.
- 💰 **DPK Dashboard:** Analisis Dana Pihak Ketiga (Tabungan, Deposito).
- 💳 **Kredit Dashboard:** Performa penyaluran kredit dan portofolio.
- 🚨 **NPL & Collection:** Monitoring Non-Performing Loan dan status kolektibilitas.
- 🏦 **Teller & Transaction:** Analisis volume transaksi harian.
- 📉 **Expense Monitoring:** Pantauan biaya operasional (Opex).
- ⚖️ **GL & Accounting:** Validasi keseimbangan neraca dan jurnal (General Ledger).
- 👥 **Customer & KYC:** Demografi nasabah dan profil risiko.
- 🛡️ **Audit & Risk:** Pemantauan indikator risiko dan kepatuhan.
- 🗣️ **Complaint Dashboard:** Rekap dan penanganan pengaduan nasabah.
- 🧹 **Data Quality:** Metrik kualitas dan kebersihan data mentah.

<br>

## 🏗️ Arsitektur Sistem Pipeline

Aplikasi ini meniru arsitektur *Enterprise Data Pipeline* dengan alur:

```mermaid
graph TD
    A[Raw Data<br/>(CSV/JSON Dummy)] -->|Validate| B(Data Validator)
    B -->|Check GL Balance & Anomalies| C{Valid?}
    C -->|No| D[Rejected Data<br/>(Validation Report)]
    C -->|Yes| E(Data Transformer)
    E -->|Clean, Aggregate, Format| F[(Data Mart Layer)]
    F --> G[Streamlit Dashboard<br/>(app.py)]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#f96,stroke:#333,stroke-width:2px
```

<br>

## 🚀 Panduan Instalasi & Penggunaan

### 1. Persiapan Environment
Pastikan Anda memiliki **Python 3.9+** terinstal di sistem Anda.
```bash
# Clone repository ini (jika belum)
git clone https://github.com/FiyyaLisanaDeV/BI-Demo.git
cd BI-Demo

# Buat virtual environment
python3 -m venv .venv

# Aktivasi virtual environment
# Untuk Linux/macOS:
source .venv/bin/activate
# Untuk Windows:
# .venv\Scripts\activate

# Install semua dependencies
pip install -r requirements.txt
```

### 2. Generate Data Dummy
Sistem membutuhkan data mentah. Jalankan script generator untuk membuat ribuan baris data transaksi dan profil nasabah:
```bash
python scripts/generate_dummy_data.py
```
*(Data akan disimpan ke dalam direktori `data/raw/`)*

### 3. Validasi Integritas Data
Pengecekan anomali (contoh: Jurnal akuntansi yang tidak balance, missing values):
```bash
python scripts/validate_data.py
```
*(Laporan data yang reject akan disimpan di `data/rejected/validation_report.xlsx`)*

### 4. Transformasi ke Data Mart
Memproses raw data yang sudah tervalidasi agar terstruktur dan ringan saat dirender oleh dashboard:
```bash
python scripts/transform_to_mart.py
```
*(Hasil olahan akan masuk ke direktori `data/mart/`)*

### 5. Jalankan Dashboard
Setelah semua tahapan ETL (Extract, Transform, Load) di atas selesai, jalankan antarmuka Streamlit:
```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

<br>

## 📁 Struktur Direktori
```text
📦 finance-bi-course
 ┣ 📂 data/             # Tempat penyimpanan Raw, Rejected, dan Data Mart
 ┣ 📂 docs/             # Dokumentasi tambahan
 ┣ 📂 pages/            # Halaman-halaman modul dashboard Streamlit
 ┣ 📂 scripts/          # Script untuk ETL & Dummy Generator
 ┣ 📂 src/              # Source code inti (Loader, Metrics, Utils, dll)
 ┣ 📜 app.py            # Entry point aplikasi Streamlit
 ┣ 📜 README.md         # Dokumentasi utama (You are here)
 ┗ 📜 requirements.txt  # Daftar dependensi library Python
```

<br>

---
<div align="center">
<i>Dibuat untuk keperluan simulasi pelatihan & demonstrasi kemahiran Data Analytics - Business Intelligence</i>
</div>
