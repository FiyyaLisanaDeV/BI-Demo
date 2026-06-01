# Format Data Dummy BPR Simulasi BPR

Dokumen ini berisi rancangan format data simulasi untuk dashboard pengolahan data BPR Simulasi BPR.

Catatan penting:

- Tidak menggunakan `branch_office`.
- Tidak menggunakan `branch_id`.
- Diasumsikan operasional berjalan sebagai **single-office / single-entity operation**.
- Pembeda data menggunakan `unit_id`, `department`, `employee_id`, `product`, `channel`, dan `area`.
- Data bersifat dummy/simulasi, bukan representasi data riil BPR Simulasi BPR.

---

## 1. Tujuan Dataset

Dataset ini disiapkan untuk simulasi:

1. Dashboard tabungan
2. Dashboard deposito
3. Dashboard kredit
4. Dashboard kolektibilitas / NPL
5. Dashboard angsuran
6. Dashboard transaksi teller
7. Dashboard kas operasional
8. Dashboard biaya operasional
9. Dashboard collection
10. Dashboard akuntansi / GL
11. Dashboard audit trail
12. Dashboard pengaduan nasabah
13. Dashboard executive summary

---

## 2. Struktur File

Disarankan membuat satu workbook Excel:

```text
bpr_simulasi_dummy_dataset.xlsx
```

Dengan sheet:

```text
01_operation_units
02_employees
03_customers
04_accounts_savings
05_accounts_deposit
06_loans
07_loan_installments
08_transactions
09_collateral
10_gl_accounts
11_gl_journal
12_collection_activity
13_expense_operational
14_audit_trail
15_customer_complaints
16_monthly_snapshot
```

---

# 01_operation_units

## Fungsi

Menyimpan daftar unit kerja internal. Ini bukan cabang, tetapi pembeda fungsi operasional.

## Grain

1 baris = 1 unit kerja.

## Kolom

```text
unit_id
unit_name
department
unit_type
manager_employee_id
is_active
```

## Contoh Value

```text
unit_id: UNIT_TELLER, UNIT_CS, UNIT_KREDIT, UNIT_COLLECTION, UNIT_DANA, UNIT_AKUNTANSI, UNIT_COMPLIANCE, UNIT_IT, UNIT_AUDIT
unit_name: Teller, Customer Service, Kredit, Collection, Dana, Akuntansi, Compliance, IT, Audit Internal
department: OPERASIONAL, KREDIT, DANA, COLLECTION, KEUANGAN, IT, COMPLIANCE, AUDIT_INTERNAL
unit_type: FRONT_OFFICE, BACK_OFFICE, CONTROL, MANAGEMENT
is_active: TRUE, FALSE
```

## Fungsi Dashboard

```text
Produktivitas per unit
Beban kerja per unit
Aktivitas transaksi per unit
Kontrol aktivitas user
```

---

# 02_employees

## Fungsi

Data pegawai, teller, customer service, account officer, kolektor, akuntansi, compliance, dan audit internal.

## Grain

1 baris = 1 pegawai.

## Kolom

```text
employee_id
full_name
unit_id
department
position
join_date
employment_status
supervisor_id
is_active
```

## Contoh Value

```text
department: OPERASIONAL, KREDIT, DANA, COLLECTION, KEUANGAN, IT, COMPLIANCE, AUDIT_INTERNAL, MANAGEMENT
position: TELLER, CUSTOMER_SERVICE, ACCOUNT_OFFICER, KOLEKTOR, KABAG_KREDIT, KABAG_OPERASIONAL, AKUNTANSI, COMPLIANCE_OFFICER, AUDITOR_INTERNAL, DIREKSI
employment_status: PERMANENT, CONTRACT, OUTSOURCE
is_active: TRUE, FALSE
```

## Fungsi Dashboard

```text
Produktivitas account officer
Produktivitas teller
Collection performance
Jumlah transaksi per pegawai
Jumlah kredit per AO
```

---

# 03_customers

## Fungsi

Data nasabah individu dan usaha.

## Grain

1 baris = 1 nasabah.

## Kolom

```text
customer_id
customer_type
full_name
gender
birth_date
age
id_type
id_number_dummy
phone_dummy
address_city
address_district
address_area
occupation
business_sector
monthly_income
risk_profile
kyc_status
customer_since
is_active
```

## Contoh Value

```text
customer_type: INDIVIDU, UMKM, BADAN_USAHA
gender: L, P
id_type: KTP, NPWP, PASPOR
address_city: KENDARI
address_district: MANDONGA, BARUGA, WUA_WUA, KADIA, POASIA, ABELI, KAMBU, PUUWATU
address_area: PASAR, PERUMAHAN, PESISIR, KAMPUS, PERKANTORAN, USAHA_MIKRO
occupation: PNS, KARYAWAN, PEDAGANG, NELAYAN, PETANI, WIRASWASTA, HONORER, IRT
business_sector: PERDAGANGAN, PERTANIAN, JASA, PERIKANAN, KONSTRUKSI, KONSUMTIF
risk_profile: LOW, MEDIUM, HIGH
kyc_status: COMPLETE, INCOMPLETE, NEED_REVIEW
is_active: TRUE, FALSE
```

## Fungsi Dashboard

```text
Jumlah nasabah
Nasabah baru
Sebaran wilayah
Profil risiko nasabah
Status KYC
Sektor usaha dominan
```

---

# 04_accounts_savings

## Fungsi

Data rekening tabungan.

## Grain

1 baris = 1 rekening tabungan.

## Kolom

```text
savings_account_id
customer_id
unit_id
product_name
open_date
current_balance
average_balance_30d
interest_rate
account_status
last_transaction_date
dormant_flag
```

## Contoh Value

```text
unit_id: UNIT_DANA, UNIT_CS, UNIT_TELLER
product_name: TABUNGAN_BAHTERAMAS, TABUNGAN_PELAJAR, TABUNGAN_UMKM, TABUNGAN_REGULER
account_status: ACTIVE, DORMANT, CLOSED, BLOCKED
dormant_flag: TRUE, FALSE
```

## Fungsi Dashboard

```text
Total DPK tabungan
Jumlah rekening aktif
Saldo rata-rata
Rekening dormant
Pertumbuhan saldo
```

---

# 05_accounts_deposit

## Fungsi

Data deposito berjangka.

## Grain

1 baris = 1 rekening deposito.

## Kolom

```text
deposit_account_id
customer_id
unit_id
product_name
placement_date
maturity_date
tenor_month
principal_amount
interest_rate
interest_payment_type
rollover_type
deposit_status
```

## Contoh Value

```text
unit_id: UNIT_DANA, UNIT_CS
product_name: DEPOSITO_1_BULAN, DEPOSITO_3_BULAN, DEPOSITO_6_BULAN, DEPOSITO_12_BULAN
tenor_month: 1, 3, 6, 12
interest_payment_type: MONTHLY, MATURITY
rollover_type: NON_ARO, ARO_PRINCIPAL, ARO_PRINCIPAL_INTEREST
deposit_status: ACTIVE, MATURED, CLOSED
```

## Fungsi Dashboard

```text
Total deposito
Deposito jatuh tempo
Komposisi tenor
Rata-rata bunga deposito
Deposito aktif vs closed
```

---

# 06_loans

## Fungsi

Data fasilitas kredit.

## Grain

1 baris = 1 kontrak kredit.

## Kolom

```text
loan_id
customer_id
unit_id
loan_product
loan_purpose
economic_sector
approval_date
disbursement_date
maturity_date
principal_amount
outstanding_principal
interest_rate
tenor_month
installment_amount
payment_frequency
collectability_status
days_past_due
loan_status
loan_officer_id
approval_status
restructure_flag
```

## Contoh Value

```text
unit_id: UNIT_KREDIT
loan_product: KREDIT_MODAL_KERJA, KREDIT_INVESTASI, KREDIT_KONSUMTIF, KREDIT_PEGAWAI, KREDIT_UMKM
loan_purpose: MODAL_USAHA, RENOVASI, KENDARAAN, PENDIDIKAN, KONSUMTIF, INVESTASI_ALAT
economic_sector: PERDAGANGAN, PERTANIAN, PERIKANAN, JASA, KONSTRUKSI, KONSUMTIF
payment_frequency: MONTHLY, WEEKLY
collectability_status: LANCAR, DPK, KURANG_LANCAR, DIRAGUKAN, MACET
loan_status: ACTIVE, PAID_OFF, WRITTEN_OFF, RESTRUCTURED
approval_status: APPROVED, REJECTED, PENDING
restructure_flag: TRUE, FALSE
```

## Fungsi Dashboard

```text
Total kredit disalurkan
Outstanding kredit
NPL
Kolektibilitas kredit
Kredit macet
Kredit jatuh tempo
Kredit restrukturisasi
Sektor ekonomi terbesar
Performa account officer
```

---

# 07_loan_installments

## Fungsi

Jadwal dan pembayaran angsuran kredit.

## Grain

1 baris = 1 angsuran.

## Kolom

```text
installment_id
loan_id
due_date
payment_date
principal_due
interest_due
penalty_due
total_due
principal_paid
interest_paid
penalty_paid
total_paid
payment_status
days_late
remaining_principal_after_payment
```

## Contoh Value

```text
payment_status: PAID, PARTIAL, UNPAID, LATE
```

## Fungsi Dashboard

```text
Angsuran jatuh tempo
Angsuran belum dibayar
Aging tunggakan
Cash inflow dari angsuran
Rasio keterlambatan
```

---

# 08_transactions

## Fungsi

Transaksi harian nasabah dan transaksi operasional.

## Grain

1 baris = 1 transaksi.

## Kolom

```text
transaction_id
transaction_date
unit_id
customer_id
account_type
account_id
transaction_type
channel
debit_credit
amount
fee_amount
transaction_status
teller_id
description
reference_no
```

## Contoh Value

```text
unit_id: UNIT_TELLER, UNIT_CS, UNIT_KREDIT, UNIT_COLLECTION, UNIT_AKUNTANSI
account_type: SAVINGS, DEPOSIT, LOAN, GL
transaction_type: SETORAN_TABUNGAN, TARIK_TUNAI, PENCAIRAN_KREDIT, BAYAR_ANGSURAN, PENEMPATAN_DEPOSITO, PENCAIRAN_DEPOSITO, BIAYA_ADMIN, KOREKSI
channel: TELLER, BACKOFFICE, KOLEKTOR, TRANSFER_BANK, MOBILE_COLLECTOR
debit_credit: DEBIT, CREDIT
transaction_status: SUCCESS, REVERSED, PENDING, FAILED
```

## Fungsi Dashboard

```text
Volume transaksi harian
Nilai transaksi harian
Aktivitas teller
Transaksi gagal
Transaksi reversal
Cash in vs cash out
```

---

# 09_collateral

## Fungsi

Data agunan kredit.

## Grain

1 baris = 1 agunan.

## Kolom

```text
collateral_id
loan_id
customer_id
collateral_type
collateral_description
estimated_value
appraised_value
binding_type
ownership_status
document_status
insurance_status
last_appraisal_date
```

## Contoh Value

```text
collateral_type: BPKB_MOTOR, BPKB_MOBIL, SERTIFIKAT_TANAH, SK_PEGAWAI, INVENTORY, DEPOSITO
binding_type: FIDUSIA, HAK_TANGGUNGAN, GADAI, KUASA_MENJUAL, NON_BINDING
ownership_status: MILIK_SENDIRI, MILIK_KELUARGA, MILIK_USAHA
document_status: COMPLETE, INCOMPLETE, EXPIRED, NEED_REVIEW
insurance_status: INSURED, NOT_INSURED, EXPIRED
```

## Fungsi Dashboard

```text
Coverage agunan
Nilai agunan vs outstanding
Dokumen agunan belum lengkap
Agunan expired
Agunan tanpa asuransi
```

---

# 10_gl_accounts

## Fungsi

Daftar akun akuntansi.

## Grain

1 baris = 1 kode akun.

## Kolom

```text
gl_account_id
gl_code
gl_name
gl_category
normal_balance
is_active
```

## Contoh Value

```text
gl_category: ASET, LIABILITAS, EKUITAS, PENDAPATAN, BEBAN
normal_balance: DEBIT, CREDIT
is_active: TRUE, FALSE
```

## Contoh Akun

```text
1001 Kas Teller
1002 Kas Besar
1101 Penempatan Pada Bank Lain
1201 Kredit Yang Diberikan
1301 Cadangan Kerugian Penurunan Nilai
2101 Tabungan Nasabah
2201 Deposito Nasabah
3101 Modal Disetor
4101 Pendapatan Bunga Kredit
4201 Pendapatan Administrasi
5101 Beban Bunga Tabungan
5102 Beban Bunga Deposito
5201 Beban Operasional
5301 Beban Penyisihan Kredit
```

## Fungsi Dashboard

```text
Saldo akun
Pendapatan bunga
Beban bunga
Beban operasional
Laba rugi sederhana
```

---

# 11_gl_journal

## Fungsi

Jurnal akuntansi.

## Grain

1 baris = 1 baris jurnal debit/kredit.

## Kolom

```text
journal_id
journal_date
unit_id
source_module
source_reference_id
gl_account_id
debit_amount
credit_amount
description
posted_by
posted_at
posting_status
```

## Contoh Value

```text
unit_id: UNIT_AKUNTANSI, UNIT_TELLER, UNIT_KREDIT, UNIT_DANA
source_module: SAVINGS, DEPOSIT, LOAN, TELLER, EXPENSE, ADJUSTMENT
posting_status: POSTED, DRAFT, REVERSED
```

## Rule Penting

```text
Total debit per journal_id harus sama dengan total credit.
```

## Fungsi Dashboard

```text
Validasi debit-kredit
Jurnal belum posting
Jurnal reversal
Pendapatan
Beban
Saldo akun
```

---

# 12_collection_activity

## Fungsi

Aktivitas penagihan kredit.

## Grain

1 baris = 1 aktivitas follow-up.

## Kolom

```text
collection_id
loan_id
customer_id
collector_id
activity_date
activity_type
contact_result
promise_to_pay_date
promise_to_pay_amount
next_follow_up_date
collection_notes
risk_escalation
```

## Contoh Value

```text
activity_type: CALL, VISIT, WHATSAPP, SURAT_PERINGATAN, NEGOSIASI, PENAGIHAN_LAPANGAN
contact_result: CONNECTED, NO_RESPONSE, PROMISE_TO_PAY, REFUSED, WRONG_NUMBER, CUSTOMER_NOT_FOUND
risk_escalation: NORMAL, WATCHLIST, LEGAL_REVIEW, RESTRUCTURE_REVIEW
```

## Fungsi Dashboard

```text
Jumlah follow-up kolektor
Kunjungan lapangan
Promise to pay
Realisasi pembayaran
Nasabah sulit dihubungi
Akun watchlist
```

---

# 13_expense_operational

## Fungsi

Biaya operasional kantor.

## Grain

1 baris = 1 pengeluaran.

## Kolom

```text
expense_id
expense_date
unit_id
department
expense_category
vendor_name
amount
payment_method
approval_status
approved_by
description
```

## Contoh Value

```text
unit_id: UNIT_OPERASIONAL, UNIT_KREDIT, UNIT_COLLECTION, UNIT_IT, UNIT_AKUNTANSI
department: OPERASIONAL, KREDIT, COLLECTION, KEUANGAN, IT, COMPLIANCE, AUDIT_INTERNAL
expense_category: ATK, LISTRIK, INTERNET, SEWA, TRANSPORT, MAINTENANCE, KONSUMSI, OPERASIONAL_KANTOR, BIAYA_PENAGIHAN, PERLENGKAPAN
payment_method: CASH, TRANSFER, PETTY_CASH
approval_status: PENDING, APPROVED, REJECTED, PAID
```

## Fungsi Dashboard

```text
Biaya operasional per unit
Biaya per kategori
Approval pending
Vendor terbesar
Cost to income sederhana
```

---

# 14_audit_trail

## Fungsi

Jejak aktivitas user di sistem.

## Grain

1 baris = 1 aksi sistem.

## Kolom

```text
audit_id
event_time
user_id
employee_id
unit_id
module_name
action_type
record_id
old_value_dummy
new_value_dummy
ip_address_dummy
device_type
risk_flag
```

## Contoh Value

```text
module_name: CUSTOMER, SAVINGS, DEPOSIT, LOAN, TRANSACTION, GL, EXPENSE, USER_MANAGEMENT
action_type: CREATE, UPDATE, DELETE, APPROVE, REJECT, LOGIN, LOGOUT, EXPORT
device_type: WEB, MOBILE, BACKOFFICE_PC
risk_flag: NORMAL, SUSPICIOUS, HIGH_RISK
```

## Fungsi Dashboard

```text
Aktivitas user
Perubahan data sensitif
Aksi high-risk
Export data
Aktivitas setelah jam kerja
```

---

# 15_customer_complaints

## Fungsi

Data pengaduan nasabah.

## Grain

1 baris = 1 pengaduan.

## Kolom

```text
complaint_id
customer_id
unit_id
complaint_date
complaint_category
complaint_channel
priority
status
resolved_date
handled_by
description
```

## Contoh Value

```text
complaint_category: SALDO, TRANSAKSI, KREDIT, DEPOSITO, PELAYANAN, BIAYA, DOKUMEN
complaint_channel: WALK_IN, PHONE, WHATSAPP, EMAIL, SURAT
priority: LOW, MEDIUM, HIGH
status: OPEN, IN_PROGRESS, RESOLVED, REJECTED
```

## Fungsi Dashboard

```text
Jumlah komplain
Komplain belum selesai
Rata-rata waktu penyelesaian
Kategori komplain terbanyak
Komplain prioritas tinggi
```

---

# 16_monthly_snapshot

## Fungsi

Snapshot bulanan untuk dashboard manajemen.

## Grain

1 baris = 1 bulan.

Karena tidak ada cabang, snapshot dibuat per bulan untuk seluruh entitas BPR.

## Kolom

```text
snapshot_month
total_customers
total_savings_balance
total_deposit_balance
total_dpk
total_loan_outstanding
total_npl_outstanding
npl_ratio
total_interest_income
total_interest_expense
total_operational_expense
profit_loss_before_tax
total_cash_balance
total_active_loans
total_dormant_accounts
total_active_employees
```

## Fungsi Dashboard

```text
Tren DPK
Tren kredit
Tren NPL
Tren laba rugi
Tren biaya operasional
Tren nasabah
Tren rekening dormant
```

---

# Relasi Antar Sheet

```text
operation_units.unit_id
    -> employees.unit_id
    -> accounts_savings.unit_id
    -> accounts_deposit.unit_id
    -> loans.unit_id
    -> transactions.unit_id
    -> gl_journal.unit_id
    -> expense_operational.unit_id
    -> audit_trail.unit_id
    -> customer_complaints.unit_id

employees.employee_id
    -> loans.loan_officer_id
    -> transactions.teller_id
    -> collection_activity.collector_id
    -> audit_trail.employee_id
    -> expense_operational.approved_by
    -> customer_complaints.handled_by

customers.customer_id
    -> accounts_savings.customer_id
    -> accounts_deposit.customer_id
    -> loans.customer_id
    -> transactions.customer_id
    -> collateral.customer_id
    -> collection_activity.customer_id
    -> customer_complaints.customer_id

loans.loan_id
    -> loan_installments.loan_id
    -> collateral.loan_id
    -> collection_activity.loan_id

gl_accounts.gl_account_id
    -> gl_journal.gl_account_id
```

---

# Jumlah Dummy Data yang Disarankan

Untuk simulasi 1.000 sampai 2.000 data, sebaiknya tidak semua sheet dipaksa 2.000 baris. Buat realistis seperti berikut:

| Sheet | Jumlah Dummy |
|---|---:|
| operation_units | 8-12 |
| employees | 30-80 |
| customers | 500-800 |
| accounts_savings | 600-1.000 |
| accounts_deposit | 100-250 |
| loans | 250-500 |
| loan_installments | 1.000-2.000 |
| transactions | 1.500-3.000 |
| collateral | 200-500 |
| gl_accounts | 30-80 |
| gl_journal | 1.000-2.000 |
| collection_activity | 300-800 |
| expense_operational | 300-700 |
| audit_trail | 1.000-2.000 |
| customer_complaints | 50-200 |
| monthly_snapshot | 12-36 |

---

# Urutan Generate Data Dummy

Agar ID relasi tidak rusak, generate data dengan urutan berikut:

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

---

# Aturan Format Tanggal

Gunakan format ISO.

```text
YYYY-MM-DD
YYYY-MM-DD HH:MM:SS
```

Contoh:

```text
2026-01-15
2026-01-15 14:35:22
```

Hindari:

```text
15/01/2026
01-15-2026
15 Januari 2026
```

---

# Aturan Format Angka

Gunakan angka murni.

Benar:

```text
12500000
350000
0.12
```

Salah:

```text
Rp 12.500.000
12,500,000
12.5 juta
12%
```

Untuk bunga, gunakan decimal:

```text
0.06 = 6%
0.12 = 12%
```

---

# Kolom yang Sebaiknya Dihitung di Python

Kolom berikut sebaiknya dihitung dari data lain, bukan diinput manual:

```text
age
days_past_due
days_late
npl_ratio
total_dpk
profit_loss_before_tax
average_balance_30d
total_cash_balance
remaining_principal_after_payment
```

---

# Field Kunci untuk Dashboard

Minimal field yang harus tersedia:

```text
customer_id
unit_id
employee_id
loan_id
account_id
transaction_date
amount
product_name
loan_product
collectability_status
days_past_due
outstanding_principal
current_balance
expense_category
gl_account_id
debit_amount
credit_amount
```

Dengan field tersebut dashboard bisa menjawab:

```text
Berapa total DPK?
Berapa total tabungan?
Berapa total deposito?
Berapa total kredit?
Berapa NPL?
Produk kredit mana paling besar?
AO mana paling produktif?
Kategori biaya terbesar apa?
Transaksi harian naik atau turun?
Nasabah mana yang menunggak?
Berapa rekening dormant?
Apakah jurnal debit-kredit balance?
Aktivitas user mana yang berisiko?
```

---

# Modul Dashboard yang Bisa Dibuat

## 1. Executive Summary

```text
Total nasabah
Total DPK
Total tabungan
Total deposito
Total kredit
Total NPL
NPL ratio
Laba rugi sebelum pajak
Total biaya operasional
```

## 2. DPK Dashboard

```text
Saldo tabungan
Saldo deposito
Komposisi produk DPK
Deposito jatuh tempo
Rekening dormant
```

## 3. Kredit Dashboard

```text
Total kredit disalurkan
Outstanding kredit
Kolektibilitas
Kredit per sektor ekonomi
Kredit per produk
Kredit restrukturisasi
```

## 4. NPL & Collection Dashboard

```text
NPL nominal
NPL ratio
Aging tunggakan
Aktivitas kolektor
Promise to pay
Watchlist account
```

## 5. Teller & Transaction Dashboard

```text
Jumlah transaksi harian
Nominal transaksi harian
Cash in
Cash out
Transaksi gagal
Transaksi reversal
Aktivitas teller
```

## 6. Expense Monitoring

```text
Biaya operasional
Biaya per kategori
Biaya per unit
Vendor terbesar
Approval pending
```

## 7. Accounting / GL Dashboard

```text
Pendapatan bunga
Beban bunga
Beban operasional
Validasi debit-kredit
Jurnal belum posting
Jurnal reversal
```

## 8. Customer & KYC Dashboard

```text
Nasabah baru
Nasabah aktif
Status KYC
Profil risiko
Sektor usaha
Sebaran wilayah
```

## 9. Audit & Risk Dashboard

```text
Aktivitas user
Aksi high-risk
Data export
Update data sensitif
Aktivitas setelah jam kerja
```

## 10. Complaint Dashboard

```text
Jumlah komplain
Status komplain
Kategori komplain
SLA penyelesaian
Komplain prioritas tinggi
```

---

# Versi Minimal Jika Ingin Mulai Cepat

Jika ingin mulai dari versi ringan, buat dulu 7 sheet:

```text
01_operation_units
02_employees
03_customers
04_accounts_savings
05_accounts_deposit
06_loans
08_transactions
```

Lalu tambahkan:

```text
07_loan_installments
09_collateral
12_collection_activity
13_expense_operational
16_monthly_snapshot
```

Terakhir tambahkan:

```text
10_gl_accounts
11_gl_journal
14_audit_trail
15_customer_complaints
```

---

# Kesimpulan Struktur

Karena tidak ada branch office, struktur simulasi BPR Simulasi BPR menjadi:

```text
Nasabah
    -> Tabungan
    -> Deposito
    -> Kredit
        -> Angsuran
        -> Agunan
        -> Collection
    -> Transaksi
    -> Komplain

Pegawai
    -> Unit Kerja
    -> Transaksi
    -> Kredit
    -> Collection
    -> Audit Trail

Transaksi
    -> GL Journal
    -> Dashboard Manajemen
```

Inti model data:

```text
customers
accounts_savings
accounts_deposit
loans
loan_installments
transactions
gl_journal
monthly_snapshot
```

Tambahan kontrol:

```text
employees
operation_units
collateral
collection_activity
expense_operational
audit_trail
customer_complaints
```
