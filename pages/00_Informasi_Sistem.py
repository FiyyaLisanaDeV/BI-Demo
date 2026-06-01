import streamlit as st

st.set_page_config(page_title="Informasi Sistem", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Informasi Sistem Finance BI BPR")

st.markdown("""
Selamat datang di **Sistem Business Intelligence Finance BPR Simulasi BPR**. Halaman ini menyajikan gambaran komprehensif mengenai arsitektur, fungsionalitas, teknologi, serta penerapan operasional dari sistem ini.

---

### 1. Deskripsi Platform
Platform ini merupakan sebuah **Sistem Business Intelligence (BI) Tersimulasi** yang dirancang secara khusus untuk memodelkan proses analitik dan operasional pada Bank Perkreditan Rakyat (BPR). Sistem ini mengintegrasikan, memproses, dan memvisualisasikan data perbankan secara *real-time*, memungkinkan pemantauan yang akurat tanpa mengekspos data rahasia nasabah yang sesungguhnya.

### 2. Tujuan dan Manfaat Sistem
Tujuan utama dari sistem ini adalah untuk menyediakan wawasan data (*data-driven insights*) yang esensial bagi jajaran manajemen tingkat menengah hingga eksekutif. Manfaat spesifik dari implementasi platform ini meliputi:
- **Pengawasan Kesehatan Finansial Bank:** Memantau rasio *Non-Performing Loan* (NPL), pertumbuhan Dana Pihak Ketiga (DPK), dan keseimbangan *General Ledger* (GL).
- **Deteksi Anomali dan Mitigasi Risiko:** Menyediakan fungsi *Audit Trail* serta validasi *Data Quality* guna memitigasi risiko manipulasi data dan mendeteksi anomali transaksi.
- **Efisiensi Pelaporan:** Mengotomatisasi proses konsolidasi data yang konvensional, sehingga pelaporan yang sebelumnya memakan waktu berhari-hari dapat diselesaikan dalam hitungan detik.

### 3. Skenario Penggunaan (Use Cases)
Sistem ini dirancang untuk mendukung berbagai fungsi krusial di dalam struktur organisasi bank, di antaranya:

- **Manajemen Kredit (Credit Management):**
  Manajer Kredit dapat memanfaatkan dasbor *NPL Collection* untuk memantau kolektibilitas pinjaman secara harian. Visibilitas ini memungkinkan identifikasi dini terhadap tren kredit bermasalah berdasarkan segmen bisnis atau portofolio *Account Officer* (AO), sehingga tindakan penagihan (*collection*) dapat dieksekusi secara presisi sebelum status pinjaman terdegradasi menjadi macet.
   
- **Kepatuhan dan Anti Pencucian Uang (Compliance & AML):**
  Divisi Kepatuhan dapat memonitor dasbor *Customer KYC* untuk mengidentifikasi nasabah dengan profil risiko tinggi (*High Risk*). Data ini dikorelasikan dengan dasbor *Transactions* untuk memantau indikasi transaksi mencurigakan, guna memastikan kepatuhan terhadap regulasi Otoritas Jasa Keuangan (OJK) dan standar pelaporan PPATK.
   
- **Manajemen Eksekutif (Executive Management / CEO):**
  Jajaran Direksi dapat memantau *Executive Summary* untuk melakukan analisis likuiditas yang komprehensif. Melalui komparasi *real-time* antara total himpunan Dana Pihak Ketiga (Inflow) dan total penyaluran Kredit (Outflow), manajemen dapat mengambil keputusan strategis terkait regulasi arus kas dengan cepat dan akurat.
   
- **Audit Internal (Internal Audit):**
  Tim Audit Internal menggunakan dasbor *Audit Risk* untuk menginvestigasi ketidaksesuaian data, seperti ketidakseimbangan neraca (*Unbalanced GL*). Sistem log aktivitas memungkinkan penelusuran rekam jejak sistem secara forensik, mengidentifikasi anomali, serta mendeteksi potensi kecurangan (*fraud*) pada tingkat operasional.

### 4. Arsitektur Teknologi (Tech Stack)
Platform ini dibangun dengan fondasi teknologi modern yang menjamin skalabilitas dan performa tinggi:
- **Antarmuka dan Visualisasi Data:** Menggunakan `Streamlit` untuk pengembangan dasbor interaktif berbasis web, yang diintegrasikan dengan `Plotly` untuk pemodelan grafik analitik tingkat lanjut.
- **Pemrosesan Data (Data Engine):** Memanfaatkan `Python` beserta pustaka `Pandas` sebagai *engine* utama untuk pemrosesan ETL (Extract, Transform, Load), agregasi, serta manipulasi data berskala besar di dalam memori.
- **Penyimpanan Data (Storage):** Mengimplementasikan format berkas modern (seperti Apache Parquet dan Excel) yang difungsikan sebagai arsitektur *Data Lake* dan *Data Warehouse* tersimulasi.
- **Infrastruktur Jaringan:** Di-*host* pada infrastruktur *server* berbasis `Linux (Ubuntu)` dan didistribusikan menggunakan *reverse-proxy* `Nginx`, didukung oleh mekanisme autentikasi keamanan *session-state* berbasis web.

### 5. Inventarisasi & Struktur Data (Berdasarkan Divisi)
Sistem ini menyimulasikan lebih dari 3.000 entitas nasabah komprehensif beserta rekam jejak historisnya. Struktur data berakar dari berbagai divisi perbankan, di antaranya:

1. **Divisi Pelayanan & Operasional (Customer Service/Teller)**
   - **Data Profil Nasabah & KYC:** Demografi (Nama, NIK, Alamat, Tanggal Lahir), sektor bisnis, serta profil risiko (Rendah/Tinggi).
   - **Transaksi Harian:** Mutasi keluar/masuk (Cash In/Cash Out) melalui teller maupun kanal digital.
   - **Pengaduan Layanan (Complaints):** Tiket komplain nasabah beserta SLA penyelesaian.
2. **Divisi Pendanaan (Funding)**
   - **Dana Pihak Ketiga (DPK):** Struktur kepemilikan rekening Tabungan dan Deposito, saldo mutasi berjalan, dan riwayat penempatan pokok deposit.
3. **Divisi Perkreditan (Lending/Credit)**
   - **Portofolio Kredit:** Data akad pinjaman, baki debet (outstanding principal), plafon kredit, dan suku bunga.
   - **Kolektibilitas & NPL:** Status kelancaran pembayaran (Lancar, DPK, Kurang Lancar, Diragukan, Macet) berdasarkan *Days Past Due* (DPD).
   - **Aktivitas Penagihan (Collection):** Catatan harian interaksi antara Petugas *Collection* dengan debitur bermasalah.
4. **Divisi Keuangan & Akuntansi (Finance/Accounting)**
   - **Jurnal Umum (General Ledger):** Catatan akuntansi *double-entry* (Debit/Kredit) dari seluruh transaksi finansial.
   - **Biaya Operasional (Opex):** Detail pengeluaran rutin bank, mulai dari gaji, utilitas, hingga pemasaran.
5. **Divisi Kepatuhan & Audit (Compliance/Internal Audit)**
   - **Audit Trail:** Log aktivitas internal (*timestamp*, identitas *user*/pegawai, jenis aksi seperti *login*, *update*, atau *delete*) untuk mendeteksi *fraud*.
6. **Divisi Sumber Daya Manusia (Human Capital)**
   - **Kinerja SDM & KPI:** Indikator Pencapaian Target (KPI) Per Pegawai Per Divisi. Mengukur rasio pencapaian target penyaluran dana (untuk manajer/staf) serta performa portofolio pegawai secara individu.

### 6. Keunggulan Platform BI vs MIS Bawaan *Core Banking*
Pertanyaan yang sering muncul adalah: *"Mengapa kita butuh BI terpisah jika Core Banking System (CBS) sudah memiliki fitur MIS (Management Information System) bawaan?"*

Berikut adalah perbedaan fundamental yang memisahkan platform *Modern BI* ini dengan MIS tradisional bawaan vendor *Core Banking*:

1. **OLAP vs OLTP (Nol Gangguan Operasional):** 
   *MIS Bawaan CBS* biasanya menembak langsung ke basis data transaksional (OLTP). Jika Direksi menarik laporan mutasi 5 tahun ke belakang, transaksi di *Teller* dan ATM bisa melambat (*lag/down*). *Sistem BI kita* menggunakan arsitektur OLAP (*Data Warehouse* terpisah), sehingga Anda bisa melakukan kalkulasi agregasi seberat apapun selama 24 jam nonstop tanpa mengganggu operasional bank sedetik pun.
2. **Kemandirian (Bebas *Vendor Lock-In*):** 
   Setiap kali Bank ingin mengubah format laporan atau menambah grafik baru di *MIS Bawaan CBS*, bank biasanya harus memanggil vendor, membayar biaya modifikasi (CR / *Change Request*) yang mahal, dan menunggu berbulan-bulan. *Sistem BI kita* dibangun dengan teknologi *open-source* (Python), sehingga tim IT internal bank dapat membuat atau mengubah dasbor dalam hitungan jam.
3. **Penggabungan Lintas-Sistem (*Multi-Source Silo Breaking*):** 
   *MIS CBS* buta terhadap data yang ada di luar sistem mereka. *Sistem BI kita* bertindak sebagai *Single Version of Truth* (Satu Sumber Kebenaran). Ia bisa menyedot data finansial dari *Core Banking*, data komplain dari aplikasi CRM, dan data performa pegawai dari sistem HRIS (SDM), lalu menggabungkannya ke dalam satu layar yang sama.
4. **Analitik Interaktif vs Laporan Statis:** 
   *MIS CBS* umumnya memuntahkan laporan akhir dalam bentuk tabel statis (PDF/Excel) yang membosankan. *Sistem BI kita* menyajikan grafika dinamis di mana pengguna bisa melakukan *Drill-Down* (mengklik grafik batang divisi tertentu untuk membedah data hingga ke tingkat pegawai atau nasabah individual secara instan).
5. **Fondasi Menuju *Artificial Intelligence* (AI):** 
   *MIS CBS* hanya mampu menengok ke masa lalu (*Descriptive Analytics*). *Sistem BI kita* menstrukturisasi data (*Feature Store/Parquet*) agar di masa depan siap disuntikkan algoritma *Machine Learning* untuk memprediksi nasabah mana yang berpotensi macet kreditnya bulan depan (*Predictive Analytics*).

### 7. Alur Pemrosesan Data (Data Workflows)
Platform ini mengadopsi arsitektur *Modern Data Pipeline* dengan struktur tiga lapis:
1. **Raw Layer (Bronze):** Entri data awal disimulasikan dan disimpan dalam bentuk tabel mentah `.xlsx` (Excel) di dalam direktori `data/raw/`. Lapisan ini menampung data sebelum melalui tahap pembersihan.
2. **Validation & Transform Layer (Silver):** Modul Validator melakukan pemindaian integritas dan konsistensi matematis (seperti validasi *Double-Entry Accounting* pada Jurnal). Apabila tervalidasi, modul Transformer akan melakukan standardisasi, agregasi, serta pembersihan data secara komputasional.
3. **Data Mart Layer (Gold):** Data yang telah matang (*ready-to-query*) dikonversi dan dipublikasikan ke dalam direktori `data/mart/`.
4. **Presentation Layer:** Modul antarmuka (*dashboard*) melakukan kueri secara langsung ke dalam *Data Mart* untuk memberikan representasi visual dalam hitungan milidetik.

### 7. Format dan Standar Data
Terdapat evolusi format penyimpanan seiring perpindahan data antar lapisan (Layer):
- **Lingkungan Mentah (Raw Environment):** Data diekstraksi menggunakan format **`.xlsx` (Excel)**. Hal ini diimplementasikan demi menjaga visibilitas operasional, agar data dasar dapat diaudit secara independen melalui aplikasi *spreadsheet* konvensional.
- **Lingkungan Analitik (Mart Environment):** Data ditransformasi ke format **`.parquet`**. Format *columnar storage* ini diaplikasikan karena memiliki efisiensi tingkat kompresi data yang sangat presisi. Kecepatan *Input/Output* (I/O) dari berkas `.parquet` terbukti secara empiris mampu memberikan performa pembacaan memori hingga 50 kali lebih cepat dibandingkan format CSV atau Excel tradisional, menjamin waktu muat (*load time*) dasbor yang optimal bagi jajaran eksekutif.
""")
