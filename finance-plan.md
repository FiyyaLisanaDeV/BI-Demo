# finance-plan.md

# Implementation Plan Dashboard Simulasi Finance BI BPR Simulasi BPR

Dokumen ini adalah rencana eksekusi bertahap untuk membangun simulasi pengolahan data BPR Simulasi BPR menggunakan:

- Python
- Streamlit
- Pandas
- Excel / CSV dummy data
- Antigravity CLI sebagai coding agent executor

Dataset yang digunakan mengacu pada format:

```text
Format_Data_Dummy_BPR_Simulasi_Kendari.md
```

Prinsip utama:

```text
Raw data tidak boleh diubah.
Data dummy boleh digenerate ulang.
Transformasi data harus dilakukan di layer processed / mart.
Dashboard hanya membaca data yang sudah divalidasi.
```

---

# 1. Target Akhir Project

Target akhir project adalah aplikasi dashboard Streamlit untuk simulasi Finance BI BPR dengan modul:

1. Executive Summary
2. DPK Dashboard
3. Kredit Dashboard
4. NPL & Collection Dashboard
5. Teller & Transaction Dashboard
6. Expense Monitoring
7. Accounting / GL Validation
8. Customer & KYC Dashboard
9. Audit & Risk Dashboard
10. Complaint Dashboard
11. Data Quality Dashboard

---

# 2. Prinsip Arsitektur

## 2.1 Arsitektur Data

```text
Dummy Generator
    -> raw/
        -> Excel / CSV mentah
    -> processed/
        -> data hasil cleaning
    -> mart/
        -> data siap dashboard
    -> Streamlit Dashboard
```

## 2.2 Larangan Utama

Agent atau script tidak boleh:

```text
Mengubah file raw secara langsung
Menimpa data mentah tanpa backup
Membuat data rahasia / data nasabah riil
Menggunakan NIK, nomor HP, alamat lengkap, atau rekening riil
Mengambil data dari internet tanpa instruksi eksplisit
Menghapus file tanpa approval
Menggabungkan semua data menjadi satu tabel besar tanpa alasan
```

## 2.3 Format Data

Gunakan format tanggal:

```text
YYYY-MM-DD
YYYY-MM-DD HH:MM:SS
```

Gunakan angka murni:

```text
12500000
0.12
350000
```

Jangan gunakan:

```text
Rp 12.500.000
12,5%
15 Januari 2026
```

---

# 3. Struktur Folder Project

Buat struktur awal:

```text
finance-bi-bpr/
├── app.py
├── requirements.txt
├── README.md
├── finance-plan.md
├── docs/
│   └── Format_Data_Dummy_BPR_Simulasi_Kendari.md
├── data/
│   ├── raw/
│   ├── processed/
│   ├── mart/
│   └── rejected/
├── notebooks/
├── scripts/
│   ├── generate_dummy_data.py
│   ├── validate_data.py
│   ├── transform_to_mart.py
│   └── export_dataset.py
├── src/
│   ├── config.py
│   ├── schema.py
│   ├── loader.py
│   ├── validator.py
│   ├── transformer.py
│   ├── metrics.py
│   └── utils.py
├── pages/
│   ├── 01_Executive_Summary.py
│   ├── 02_DPK_Dashboard.py
│   ├── 03_Kredit_Dashboard.py
│   ├── 04_NPL_Collection.py
│   ├── 05_Transactions.py
│   ├── 06_Expense_Monitoring.py
│   ├── 07_GL_Accounting.py
│   ├── 08_Customer_KYC.py
│   ├── 09_Audit_Risk.py
│   ├── 10_Complaints.py
│   └── 11_Data_Quality.py
└── tests/
    ├── test_schema.py
    ├── test_validation.py
    ├── test_metrics.py
    └── test_gl_balance.py
```

---

# 4. Tech Stack

## 4.1 Python Packages

Isi `requirements.txt`:

```text
streamlit
pandas
numpy
openpyxl
xlsxwriter
plotly
faker
python-dateutil
pydantic
pytest
```

Opsional:

```text
duckdb
pyarrow
```

Gunakan DuckDB jika dataset mulai besar atau ingin query SQL lokal.

---

# 5. Cara Eksekusi dengan Antigravity CLI

## 5.1 Pola Kerja

Jalankan Antigravity CLI dari root project:

```bash
cd finance-bi-bpr
agy
```

Gunakan pola instruksi:

```text
Kerjakan hanya tahap yang saya minta.
Jangan lompat ke tahap berikutnya.
Jangan hapus file.
Jangan ubah raw data.
Setiap selesai tahap, tampilkan file yang dibuat/diubah dan cara mengetesnya.
```

## 5.2 Prompt Dasar untuk Agent

Gunakan prompt pembuka berikut di Antigravity CLI:

```text
Kamu adalah coding agent untuk project Finance BI BPR Simulasi BPR.

Ikuti finance-plan.md sebagai sumber instruksi utama.

Aturan:
1. Kerjakan bertahap.
2. Jangan mengubah data raw secara langsung.
3. Jangan menggunakan data nasabah riil.
4. Jangan menghapus file tanpa approval.
5. Buat kode yang sederhana, modular, dan mudah dibaca.
6. Setiap fungsi penting harus punya docstring singkat.
7. Setiap tahap harus bisa dites dengan command yang jelas.
8. Jika ada asumsi, tulis di README atau komentar kode.
9. Jangan membuat dependency berat tanpa alasan.
10. Prioritaskan pandas + streamlit + plotly.

Mulai dari tahap yang saya instruksikan berikutnya.
```

---

# 6. Tahap 0 — Inisialisasi Project

## Tujuan

Membuat struktur folder dan file dasar.

## Output

```text
finance-bi-bpr/
requirements.txt
README.md
app.py
src/
scripts/
pages/
tests/
data/
docs/
```

## Prompt untuk Antigravity CLI

```text
Buat struktur project Streamlit untuk Finance BI BPR sesuai finance-plan.md.

Tugas:
1. Buat folder: data/raw, data/processed, data/mart, data/rejected, scripts, src, pages, tests, docs, notebooks.
2. Buat requirements.txt.
3. Buat README.md ringkas.
4. Buat app.py sederhana dengan judul "Finance BI BPR Simulasi BPR".
5. Buat src/config.py berisi path folder utama.
6. Jangan membuat data dummy dulu.
7. Jangan membuat dashboard lengkap dulu.

Setelah selesai, tampilkan daftar file yang dibuat dan cara menjalankan app.
```

## Acceptance Criteria

```text
streamlit run app.py berhasil
Folder data tersedia
requirements.txt tersedia
README.md tersedia
Tidak ada error import
```

---

# 7. Tahap 1 — Definisi Schema

## Tujuan

Membuat definisi schema untuk semua sheet/tabel.

## Output

```text
src/schema.py
tests/test_schema.py
```

## Tabel yang Harus Didukung

```text
operation_units
employees
customers
accounts_savings
accounts_deposit
loans
loan_installments
transactions
collateral
gl_accounts
gl_journal
collection_activity
expense_operational
audit_trail
customer_complaints
monthly_snapshot
```

## Prompt untuk Antigravity CLI

```text
Implementasikan src/schema.py berdasarkan finance-plan.md dan docs/Format_Data_Dummy_BPR_Simulasi_Kendari.md.

Tugas:
1. Buat dictionary REQUIRED_COLUMNS untuk setiap tabel.
2. Buat dictionary COLUMN_TYPES untuk tipe data utama.
3. Buat dictionary ENUM_VALUES untuk kolom enum penting.
4. Buat function get_required_columns(table_name).
5. Buat function list_tables().
6. Buat test sederhana di tests/test_schema.py.

Jangan generate data dulu.
Jangan membuat dashboard dulu.
```

## Acceptance Criteria

```text
pytest tests/test_schema.py berhasil
Semua tabel memiliki required columns
Tidak ada branch_id
Tidak ada branch_office
Semua relasi menggunakan unit_id, customer_id, employee_id, loan_id
```

---

# 8. Tahap 2 — Dummy Data Generator

## Tujuan

Membuat script generate data dummy 1.000–2.000 baris per tabel utama sesuai kebutuhan simulasi.

## Output

```text
scripts/generate_dummy_data.py
data/raw/bpr_simulasi_dummy_dataset.xlsx
data/raw/*.csv
```

## Prinsip Generate

Generate berurutan:

```text
1. operation_units
2. employees
3. customers
4. accounts_savings
5. accounts_deposit
6. loans
7. loan_installments
8. collateral
9. transactions
10. gl_accounts
11. gl_journal
12. collection_activity
13. expense_operational
14. audit_trail
15. customer_complaints
16. monthly_snapshot
```

## Volume Awal

```text
operation_units: 10
employees: 50
customers: 700
accounts_savings: 900
accounts_deposit: 180
loans: 400
loan_installments: 1600
transactions: 2500
collateral: 350
gl_accounts: 50
gl_journal: 1600
collection_activity: 600
expense_operational: 500
audit_trail: 1500
customer_complaints: 120
monthly_snapshot: 24
```

## Prompt untuk Antigravity CLI

```text
Buat scripts/generate_dummy_data.py.

Tugas:
1. Generate data dummy sesuai schema.py.
2. Jangan gunakan data pribadi riil.
3. Gunakan Faker untuk nama dan data dummy umum.
4. Gunakan ID konsisten seperti CUST000001, LOAN000001, EMP000001.
5. Pastikan tidak ada branch_id dan tidak ada branch_office.
6. Pastikan relasi customer_id, employee_id, unit_id, loan_id valid.
7. Export ke satu Excel workbook di data/raw/bpr_simulasi_dummy_dataset.xlsx.
8. Export juga masing-masing tabel ke CSV di data/raw/.
9. Buat parameter jumlah data di bagian atas script.
10. Tambahkan seed agar hasil bisa direproduksi.

Jangan membuat dashboard dulu.
```

## Acceptance Criteria

```text
python scripts/generate_dummy_data.py berhasil
File Excel terbentuk
CSV tiap tabel terbentuk
Jumlah data sesuai parameter
Tidak ada ID relasi yang kosong
Tidak ada data pribadi riil
```

---

# 9. Tahap 3 — Data Validator

## Tujuan

Membuat validator untuk mengecek kelengkapan kolom, tipe data, enum, relasi, dan kualitas data.

## Output

```text
src/validator.py
scripts/validate_data.py
data/rejected/validation_report.xlsx
tests/test_validation.py
```

## Validasi Wajib

```text
Kolom wajib tersedia
Tidak ada branch_id
Tidak ada branch_office
Tanggal valid
Nominal numerik
Enum valid
customer_id valid
employee_id valid
unit_id valid
loan_id valid
GL debit-credit balance
Tidak ada outstanding negatif
Tidak ada saldo tabungan negatif
Tidak ada tenor <= 0
Tidak ada interest_rate negatif
```

## Prompt untuk Antigravity CLI

```text
Buat modul validator.

Tugas:
1. Buat src/validator.py.
2. Buat scripts/validate_data.py.
3. Validator membaca data/raw/bpr_simulasi_dummy_dataset.xlsx.
4. Cek required columns berdasarkan src/schema.py.
5. Cek tipe data dasar.
6. Cek enum values.
7. Cek foreign key antar tabel.
8. Cek GL journal: total debit harus sama dengan total credit per journal_id.
9. Simpan validation report ke data/rejected/validation_report.xlsx.
10. Tampilkan ringkasan validasi di terminal.

Jangan mengubah file raw.
Jangan membuat dashboard dulu.
```

## Acceptance Criteria

```text
python scripts/validate_data.py berhasil
validation_report.xlsx terbentuk
Jika data valid, status PASS
Jika data invalid, error detail per tabel tersedia
GL balance check tersedia
```

---

# 10. Tahap 4 — Transformasi ke Data Mart

## Tujuan

Membuat layer data siap dashboard.

## Output

```text
src/transformer.py
scripts/transform_to_mart.py
data/mart/*.csv
data/mart/*.xlsx
```

## Mart yang Dibuat

```text
mart_executive_summary
mart_dpk
mart_loans
mart_npl
mart_transactions
mart_collection
mart_expense
mart_gl
mart_customer_kyc
mart_audit
mart_complaints
mart_data_quality
```

## Prompt untuk Antigravity CLI

```text
Buat transformasi data mart.

Tugas:
1. Buat src/transformer.py.
2. Buat scripts/transform_to_mart.py.
3. Baca data dari data/raw/bpr_simulasi_dummy_dataset.xlsx.
4. Jangan ubah data raw.
5. Buat mart untuk executive summary, DPK, loan, NPL, transactions, collection, expense, GL, customer KYC, audit, complaints, data quality.
6. Simpan hasil mart ke data/mart/ dalam format CSV.
7. Buat juga data/mart/bpr_simulasi_mart.xlsx.
8. Pastikan setiap mart punya kolom tanggal/bulan jika relevan.
9. Pastikan perhitungan NPL ratio benar.
10. Pastikan total_dpk = total_savings_balance + total_deposit_balance.

Jangan membuat UI lengkap dulu.
```

## Acceptance Criteria

```text
python scripts/transform_to_mart.py berhasil
CSV mart terbentuk
Excel mart terbentuk
Tidak ada perubahan file raw
NPL ratio terhitung
Total DPK terhitung
```

---

# 11. Tahap 5 — Core Metrics

## Tujuan

Membuat fungsi KPI agar dashboard tidak menghitung ulang secara acak.

## Output

```text
src/metrics.py
tests/test_metrics.py
```

## KPI Wajib

```text
total_customers
total_savings_balance
total_deposit_balance
total_dpk
total_loan_outstanding
total_npl_outstanding
npl_ratio
total_transactions
total_transaction_amount
cash_in
cash_out
total_operational_expense
interest_income
interest_expense
profit_loss_before_tax
gl_balance_status
dormant_account_count
kyc_incomplete_count
high_risk_audit_count
open_complaint_count
```

## Prompt untuk Antigravity CLI

```text
Buat src/metrics.py dan tests/test_metrics.py.

Tugas:
1. Buat fungsi KPI reusable.
2. Fungsi menerima DataFrame, bukan membaca file langsung.
3. Buat unit test untuk NPL ratio, total DPK, cash in/out, dan GL balance.
4. Hindari duplikasi logika dengan transformer.
5. Dokumentasikan rumus singkat di docstring.

Jangan membuat UI dulu.
```

## Acceptance Criteria

```text
pytest tests/test_metrics.py berhasil
Rumus KPI jelas
Fungsi tidak membaca file langsung
```

---

# 12. Tahap 6 — Streamlit App Shell

## Tujuan

Membuat kerangka utama aplikasi Streamlit.

## Output

```text
app.py
src/loader.py
pages/*.py placeholder
```

## Prompt untuk Antigravity CLI

```text
Bangun shell Streamlit app.

Tugas:
1. Update app.py dengan layout wide.
2. Buat src/loader.py untuk load data mart dengan st.cache_data.
3. Buat sidebar info dataset.
4. Buat landing page berisi ringkasan project.
5. Buat semua file pages sebagai placeholder dengan judul masing-masing.
6. Jangan isi grafik kompleks dulu.
7. Dashboard harus bisa dijalankan dengan streamlit run app.py.

Gunakan data dari data/mart/.
Jika data/mart belum ada, tampilkan pesan agar user menjalankan transform_to_mart.py.
```

## Acceptance Criteria

```text
streamlit run app.py berhasil
Semua halaman muncul di sidebar Streamlit
Tidak error jika data belum ada
Loader menggunakan cache
```

---

# 13. Tahap 7 — Executive Summary Dashboard

## Tujuan

Membangun halaman ringkasan eksekutif.

## Output

```text
pages/01_Executive_Summary.py
```

## Komponen

```text
KPI cards
Trend DPK
Trend kredit
Trend NPL
Trend laba rugi
Ringkasan kesehatan data
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/01_Executive_Summary.py.

Tugas:
1. Load mart_executive_summary dan monthly_snapshot.
2. Tampilkan KPI cards:
   - Total nasabah
   - Total DPK
   - Total kredit
   - NPL ratio
   - Laba rugi sebelum pajak
   - Rekening dormant
3. Tampilkan chart trend bulanan:
   - DPK
   - Kredit outstanding
   - NPL ratio
   - Profit/loss before tax
4. Tambahkan filter bulan.
5. Gunakan Plotly untuk chart.
6. Buat tampilan rapi dan sederhana.

Jangan mengubah data mart.
```

## Acceptance Criteria

```text
Halaman executive summary tampil
KPI sesuai data mart
Filter bulan bekerja
Chart tampil tanpa error
```

---

# 14. Tahap 8 — DPK Dashboard

## Tujuan

Membangun dashboard dana pihak ketiga.

## Output

```text
pages/02_DPK_Dashboard.py
```

## Komponen

```text
Total tabungan
Total deposito
Total DPK
Komposisi produk tabungan
Komposisi tenor deposito
Deposito jatuh tempo
Rekening dormant
Top nasabah berdasarkan saldo dummy
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/02_DPK_Dashboard.py.

Tugas:
1. Load accounts_savings, accounts_deposit, customers, dan mart_dpk.
2. Buat KPI total tabungan, total deposito, total DPK.
3. Buat chart komposisi produk tabungan.
4. Buat chart komposisi tenor deposito.
5. Buat tabel deposito jatuh tempo 30 hari.
6. Buat tabel rekening dormant.
7. Buat filter product_name dan status.
8. Jangan tampilkan data pribadi sensitif selain dummy ID dan nama dummy.

Pastikan halaman tidak error jika data kosong.
```

## Acceptance Criteria

```text
KPI DPK tampil
Chart produk tampil
Deposito jatuh tempo muncul
Dorman account terdeteksi
Filter bekerja
```

---

# 15. Tahap 9 — Kredit Dashboard

## Tujuan

Membangun dashboard kredit.

## Output

```text
pages/03_Kredit_Dashboard.py
```

## Komponen

```text
Total principal
Outstanding principal
Kredit aktif
Kredit lunas
Kredit restrukturisasi
Kredit per produk
Kredit per sektor ekonomi
Performa account officer
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/03_Kredit_Dashboard.py.

Tugas:
1. Load loans, customers, employees, dan mart_loans.
2. KPI:
   - Total kredit disalurkan
   - Outstanding kredit
   - Kredit aktif
   - Kredit restrukturisasi
   - Rata-rata ticket size
3. Chart:
   - Kredit per produk
   - Kredit per sektor ekonomi
   - Outstanding per kolektibilitas
4. Tabel:
   - Top 20 kredit outstanding
   - Performa account officer
5. Filter:
   - loan_product
   - economic_sector
   - loan_status
   - collectability_status
6. Jangan mengubah data mart.
```

## Acceptance Criteria

```text
Dashboard kredit tampil
Filter bekerja
Outstanding cocok dengan data
AO performance tampil
```

---

# 16. Tahap 10 — NPL & Collection Dashboard

## Tujuan

Membangun dashboard kualitas kredit dan penagihan.

## Output

```text
pages/04_NPL_Collection.py
```

## Komponen

```text
NPL nominal
NPL ratio
Kolektibilitas
Days past due bucket
Aktivitas kolektor
Promise to pay
Watchlist account
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/04_NPL_Collection.py.

Tugas:
1. Load loans, loan_installments, collection_activity, customers, employees.
2. Hitung NPL:
   - collectability_status KURANG_LANCAR, DIRAGUKAN, MACET dianggap NPL.
3. Buat KPI:
   - NPL nominal
   - NPL ratio
   - Jumlah loan NPL
   - Total promise to pay
   - Watchlist count
4. Buat DPD bucket:
   - 0
   - 1-30
   - 31-60
   - 61-90
   - >90
5. Chart kolektibilitas.
6. Tabel akun menunggak.
7. Tabel aktivitas collector.
8. Filter collector, status kolektibilitas, DPD bucket.

Jangan membuat keputusan kredit otomatis.
Dashboard hanya analitik.
```

## Acceptance Criteria

```text
NPL ratio benar
DPD bucket tampil
Collection activity tampil
Watchlist tampil
```

---

# 17. Tahap 11 — Teller & Transaction Dashboard

## Tujuan

Membangun dashboard transaksi harian.

## Output

```text
pages/05_Transactions.py
```

## Komponen

```text
Volume transaksi
Nominal transaksi
Cash in
Cash out
Transaksi gagal
Transaksi reversal
Aktivitas teller
Channel transaksi
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/05_Transactions.py.

Tugas:
1. Load transactions, employees, customers.
2. KPI:
   - Total transaksi
   - Total nominal transaksi
   - Cash in
   - Cash out
   - Failed transaction count
   - Reversed transaction count
3. Chart:
   - Trend transaksi harian
   - Transaksi per type
   - Transaksi per channel
   - Aktivitas teller
4. Filter:
   - tanggal
   - transaction_type
   - channel
   - transaction_status
   - teller
5. Tampilkan tabel detail transaksi.

Jangan tampilkan informasi pribadi riil.
```

## Acceptance Criteria

```text
Transaksi harian tampil
Cash in/out benar
Filter tanggal bekerja
Teller performance tampil
```

---

# 18. Tahap 12 — Expense Monitoring

## Tujuan

Membangun dashboard pengeluaran operasional.

## Output

```text
pages/06_Expense_Monitoring.py
```

## Komponen

```text
Total biaya
Biaya per kategori
Biaya per unit
Approval pending
Vendor terbesar
Trend biaya bulanan
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/06_Expense_Monitoring.py.

Tugas:
1. Load expense_operational dan operation_units.
2. KPI:
   - Total biaya
   - Jumlah transaksi biaya
   - Approval pending
   - Vendor terbesar
3. Chart:
   - Biaya per kategori
   - Biaya per unit
   - Trend biaya bulanan
4. Tabel:
   - Top vendor
   - Pending approval
5. Filter:
   - expense_category
   - department
   - approval_status
   - payment_method
```

## Acceptance Criteria

```text
Expense dashboard tampil
Pending approval tampil
Trend biaya tampil
Top vendor tampil
```

---

# 19. Tahap 13 — GL & Accounting Validation

## Tujuan

Membangun dashboard akuntansi dan validasi jurnal.

## Output

```text
pages/07_GL_Accounting.py
```

## Komponen

```text
Debit-credit balance
Jurnal belum posting
Jurnal reversal
Pendapatan bunga
Beban bunga
Beban operasional
Trial balance sederhana
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/07_GL_Accounting.py.

Tugas:
1. Load gl_accounts dan gl_journal.
2. Validasi total debit dan credit per journal_id.
3. Tampilkan KPI:
   - Total debit
   - Total credit
   - Selisih debit-credit
   - Jumlah jurnal tidak balance
   - Jurnal draft
   - Jurnal reversal
4. Buat trial balance sederhana per gl_account.
5. Chart pendapatan vs beban.
6. Tabel jurnal tidak balance.
7. Filter source_module dan posting_status.

Jangan memperbaiki jurnal otomatis.
Hanya tampilkan validasi.
```

## Acceptance Criteria

```text
GL balance check tampil
Trial balance tampil
Jurnal tidak balance terdeteksi
Tidak ada auto-correction
```

---

# 20. Tahap 14 — Customer & KYC Dashboard

## Tujuan

Membangun dashboard nasabah dan KYC.

## Output

```text
pages/08_Customer_KYC.py
```

## Komponen

```text
Total nasabah
Nasabah aktif
Nasabah baru
Status KYC
Risk profile
Sektor usaha
Sebaran wilayah
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/08_Customer_KYC.py.

Tugas:
1. Load customers.
2. KPI:
   - Total nasabah
   - Nasabah aktif
   - Nasabah baru bulan berjalan
   - KYC incomplete
   - High risk customer
3. Chart:
   - Customer type
   - KYC status
   - Risk profile
   - Business sector
   - Address district
4. Tabel:
   - Nasabah need review
   - Nasabah high risk
5. Filter:
   - customer_type
   - kyc_status
   - risk_profile
   - business_sector
```

## Acceptance Criteria

```text
KYC dashboard tampil
High risk customer tampil
Need review tampil
Filter bekerja
```

---

# 21. Tahap 15 — Audit & Risk Dashboard

## Tujuan

Membangun dashboard audit trail dan aktivitas berisiko.

## Output

```text
pages/09_Audit_Risk.py
```

## Komponen

```text
Aktivitas user
Login/logout
Export data
Update data sensitif
Delete action
High risk event
Aktivitas setelah jam kerja
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/09_Audit_Risk.py.

Tugas:
1. Load audit_trail, employees, operation_units.
2. KPI:
   - Total event
   - High risk event
   - Suspicious event
   - Export action
   - Delete action
   - After-hours activity
3. Chart:
   - Event by module
   - Event by action type
   - Event by hour
   - Event by employee
4. Tabel:
   - High risk activity
   - Activity after office hour
   - Export events
5. Filter:
   - module_name
   - action_type
   - risk_flag
   - employee
```

## Acceptance Criteria

```text
Audit dashboard tampil
High risk event terlihat
After-hours activity terdeteksi
Filter bekerja
```

---

# 22. Tahap 16 — Complaint Dashboard

## Tujuan

Membangun dashboard pengaduan nasabah.

## Output

```text
pages/10_Complaints.py
```

## Komponen

```text
Jumlah komplain
Komplain open
Komplain high priority
Rata-rata waktu penyelesaian
Kategori komplain
Channel komplain
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/10_Complaints.py.

Tugas:
1. Load customer_complaints, customers, employees.
2. KPI:
   - Total complaints
   - Open complaints
   - High priority complaints
   - Resolved complaints
   - Average resolution days
3. Chart:
   - Complaint by category
   - Complaint by channel
   - Complaint by status
   - Complaint trend
4. Tabel:
   - Open complaints
   - High priority complaints
5. Filter:
   - status
   - priority
   - complaint_category
   - complaint_channel
```

## Acceptance Criteria

```text
Complaint dashboard tampil
SLA sederhana tampil
Open complaint terdeteksi
Filter bekerja
```

---

# 23. Tahap 17 — Data Quality Dashboard

## Tujuan

Membangun dashboard kualitas data.

## Output

```text
pages/11_Data_Quality.py
```

## Komponen

```text
Missing values
Duplicate rows
Invalid enum
Invalid foreign key
Invalid date
Invalid numeric
GL imbalance
Data completeness score
```

## Prompt untuk Antigravity CLI

```text
Implementasikan pages/11_Data_Quality.py.

Tugas:
1. Load validation_report.xlsx jika tersedia.
2. Jika validation_report belum ada, tampilkan instruksi menjalankan validate_data.py.
3. Tampilkan KPI:
   - Total checks
   - Passed checks
   - Failed checks
   - Warning count
   - Data quality score
4. Tampilkan tabel error per table.
5. Tampilkan chart failed checks by table.
6. Tambahkan tombol informasi cara regenerate data dan validate ulang.

Jangan menjalankan script otomatis dari dashboard.
Dashboard hanya membaca report.
```

## Acceptance Criteria

```text
Validation report terbaca
Data quality score tampil
Error table tampil
Tidak auto-run script
```

---

# 24. Tahap 18 — Export & Download

## Tujuan

Membuat fitur download hasil filter dan data mart.

## Output

```text
src/utils.py
Update pages terkait
```

## Prompt untuk Antigravity CLI

```text
Tambahkan fitur export/download.

Tugas:
1. Buat helper convert_df_to_csv di src/utils.py.
2. Tambahkan tombol download CSV pada setiap halaman utama.
3. Export hanya data hasil filter, bukan seluruh raw data.
4. Nama file download harus jelas.
5. Jangan membuat fitur upload/overwrite raw data.
```

## Acceptance Criteria

```text
Download CSV bekerja
File hasil filter bisa dibuka
Raw data tidak berubah
```

---

# 25. Tahap 19 — Testing & Quality Gate

## Tujuan

Memastikan project stabil.

## Output

```text
tests/
README update
```

## Checklist Test

```text
pytest berjalan
streamlit app berjalan
generate_dummy_data.py berjalan
validate_data.py berjalan
transform_to_mart.py berjalan
Semua halaman dashboard bisa dibuka
Tidak ada branch_id
Tidak ada data riil
GL balance check bekerja
NPL ratio benar
```

## Prompt untuk Antigravity CLI

```text
Lakukan testing project.

Tugas:
1. Jalankan pytest.
2. Jalankan generate_dummy_data.py.
3. Jalankan validate_data.py.
4. Jalankan transform_to_mart.py.
5. Periksa import error pada semua halaman Streamlit.
6. Perbaiki error kecil yang ditemukan.
7. Jangan mengubah desain besar tanpa instruksi.
8. Update README dengan cara menjalankan project.

Tampilkan ringkasan hasil test.
```

## Acceptance Criteria

```text
pytest pass
Script utama pass
README lengkap
Tidak ada error import
```

---

# 26. Tahap 20 — Final Hardening

## Tujuan

Merapikan project agar siap dipresentasikan.

## Output

```text
README.md final
requirements.txt final
data sample tersedia
dashboard stabil
```

## Prompt untuk Antigravity CLI

```text
Lakukan final hardening.

Tugas:
1. Rapikan README.
2. Pastikan requirements.txt tidak berisi dependency tidak terpakai.
3. Tambahkan catatan bahwa data adalah dummy.
4. Tambahkan cara generate ulang data.
5. Tambahkan cara validasi data.
6. Tambahkan cara transform ke mart.
7. Tambahkan cara menjalankan Streamlit.
8. Pastikan semua halaman punya judul dan deskripsi singkat.
9. Jangan menambah fitur baru.
```

## Acceptance Criteria

```text
Project bisa dipresentasikan
Instruksi jelas
Data dummy tersedia
Dashboard berjalan stabil
```

---

# 27. Command Eksekusi Manual

## Install Dependency

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Generate Data

```bash
python scripts/generate_dummy_data.py
```

## Validasi Data

```bash
python scripts/validate_data.py
```

## Transformasi Data Mart

```bash
python scripts/transform_to_mart.py
```

## Jalankan Dashboard

```bash
streamlit run app.py
```

## Test

```bash
pytest
```

---

# 28. Checklist Harian Saat Eksekusi

Sebelum meminta agent menulis kode:

```text
Apakah tahap yang diminta jelas?
Apakah output file jelas?
Apakah ada larangan eksplisit?
Apakah acceptance criteria jelas?
```

Setelah agent selesai:

```text
Cek file yang berubah
Jalankan test
Jalankan script terkait
Buka dashboard
Cek apakah raw data berubah
Commit perubahan jika stabil
```

---

# 29. Commit Plan

Gunakan commit kecil per tahap:

```bash
git add .
git commit -m "init project structure"

git add .
git commit -m "add schema definitions"

git add .
git commit -m "add dummy data generator"

git add .
git commit -m "add data validation"

git add .
git commit -m "add mart transformation"

git add .
git commit -m "add streamlit app shell"

git add .
git commit -m "add executive summary dashboard"
```

---

# 30. Prioritas Eksekusi Paling Aman

Jika ingin cepat jadi demo, jalankan urutan ini dulu:

```text
Tahap 0: Init project
Tahap 1: Schema
Tahap 2: Dummy generator
Tahap 3: Validator
Tahap 4: Data mart
Tahap 6: Streamlit shell
Tahap 7: Executive Summary
Tahap 8: DPK Dashboard
Tahap 9: Kredit Dashboard
Tahap 10: NPL & Collection Dashboard
```

Setelah itu baru lanjut:

```text
Transactions
Expense
GL
Customer KYC
Audit Risk
Complaints
Data Quality
Export
Testing
Hardening
```

---

# 31. Batasan Analitik

Dashboard ini hanya untuk simulasi:

```text
Tidak digunakan untuk keputusan kredit riil
Tidak digunakan untuk penilaian nasabah riil
Tidak digunakan untuk pelaporan resmi OJK
Tidak menggunakan data nasabah asli
Tidak menggantikan core banking
```

Fungsi dashboard:

```text
Membaca data
Membersihkan data
Meringkas data
Membuat visualisasi
Menguji kualitas data
Membantu presentasi konsep Finance BI
```

---

# 32. Definition of Done

Project dianggap selesai jika:

```text
Data dummy bisa digenerate
Data dummy bisa divalidasi
Data mart bisa dibuat
Dashboard Streamlit bisa berjalan
Semua halaman utama bisa dibuka
Executive Summary menampilkan KPI utama
DPK dashboard berjalan
Kredit dashboard berjalan
NPL dashboard berjalan
Transaction dashboard berjalan
Expense dashboard berjalan
GL dashboard berjalan
Audit dashboard berjalan
Data Quality dashboard berjalan
README jelas
Tidak ada data riil
Tidak ada branch_id
Tidak ada branch_office
Raw data tidak dimodifikasi oleh dashboard
```

---

# 33. Prompt Final untuk Review Agent

Gunakan prompt ini setelah semua tahap selesai:

```text
Review seluruh project Finance BI BPR.

Cek:
1. Apakah semua instruksi finance-plan.md sudah dipenuhi?
2. Apakah masih ada branch_id atau branch_office?
3. Apakah ada data pribadi riil?
4. Apakah raw data pernah dimodifikasi?
5. Apakah schema, validator, transformer, metrics, dan dashboard konsisten?
6. Apakah semua halaman Streamlit bisa dibuka?
7. Apakah README sudah cukup untuk user menjalankan project?
8. Apakah ada dependency tidak terpakai?
9. Apakah ada fungsi yang terlalu kompleks?
10. Apakah ada risiko agent/destructive operation?

Jangan membuat perubahan besar.
Berikan daftar temuan dan patch kecil jika diperlukan.
```

---

# 34. Catatan Desain

Desain ini sengaja memakai struktur modular agar mudah dipahami:

```text
schema.py      -> definisi kolom
validator.py   -> pemeriksaan data
transformer.py -> data mart
metrics.py     -> rumus KPI
loader.py      -> load data dashboard
pages/         -> UI Streamlit
scripts/       -> eksekusi data pipeline
tests/         -> quality gate
```

Jangan mencampur semua logic di `app.py`.

`app.py` hanya untuk landing page dan konfigurasi utama.

---

# 35. Ringkasan Eksekusi

Urutan kerja paling ringkas:

```text
1. Buat struktur project
2. Buat schema
3. Generate dummy data
4. Validasi dummy data
5. Transform ke data mart
6. Buat Streamlit shell
7. Buat dashboard Executive
8. Buat dashboard DPK
9. Buat dashboard Kredit
10. Buat dashboard NPL
11. Tambahkan modul lain
12. Test
13. Final hardening
```

Tujuan akhirnya bukan sekadar dashboard visual, tetapi simulasi alur BI yang benar:

```text
Data mentah
    -> Validasi
    -> Transformasi
    -> Data mart
    -> KPI
    -> Dashboard
    -> Export hasil filter
```
