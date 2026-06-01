# Finance BI BPR Simulasi BPR (Simulasi)

Project ini adalah **Dashboard Simulasi Business Intelligence** untuk pengolahan data BPR Simulasi BPR.

⚠️ **PENTING: Seluruh data yang ada dalam repository ini adalah DATA DUMMY hasil generate sistem (Faker). Tidak ada data pribadi asli, NIK, atau data rahasia nasabah sungguhan.** ⚠️

## 🏗️ Struktur Arsitektur
Sistem ini meniru pipeline data enterprise:
1. **Raw Data:** Data mentah hasil generate dummy
2. **Data Validator:** Mengecek integritas (GL Balance, kelengkapan kolom)
3. **Data Transformer:** Memproses raw data menjadi layer Data Mart
4. **Streamlit Dashboard:** Menampilkan insight berdasarkan Data Mart

## 🚀 Cara Menjalankan Project

### 1. Persiapan Environment
Pastikan Anda sudah menginstall Python 3.9+. Buat virtual environment dan install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Data Dummy
Jika Anda ingin me-reset atau menggenerate ulang ribuan data dummy:
```bash
python scripts/generate_dummy_data.py
```
*(Data akan masuk ke folder `data/raw/`)*

### 3. Validasi Data
Script ini akan membaca raw data dan mengecek anomali, seperti jurnal yang tidak balance:
```bash
python scripts/validate_data.py
```
*(Report akan masuk ke `data/rejected/validation_report.xlsx`)*

### 4. Transformasi ke Data Mart
Memproses raw data agar lebih ringan dan siap dibaca oleh Dashboard:
```bash
python scripts/transform_to_mart.py
```
*(Hasil mart akan masuk ke folder `data/mart/`)*

### 5. Jalankan Dashboard Streamlit
```bash
streamlit run app.py
```

## 📊 Modul Dashboard
Sistem ini dilengkapi dengan 11 modul utama:
- Executive Summary
- DPK Dashboard
- Kredit Dashboard
- NPL & Collection Dashboard
- Teller & Transaction Dashboard
- Expense Monitoring
- GL & Accounting Validation
- Customer & KYC
- Audit & Risk
- Complaint Dashboard
- Data Quality Dashboard
