import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="Finance BI Hub untuk BPR/BPRS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
        
        html, body, .stApp {
            font-family: 'Outfit', sans-serif;
            background-color: #f8fafc;
        }
        
        #MainMenu, footer {
            visibility: hidden;
            height: 0;
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(226, 232, 240, 0.8);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
            margin-bottom: 1.25rem;
        }
        
        .gradient-text {
            background: linear-gradient(90deg, #0f172a, #10b981, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.2rem;
            margin-bottom: 1rem;
        }
        
        .custom-progress-container {
            width: 100%;
            background-color: #e2e8f0;
            border-radius: 999px;
            height: 10px;
            margin-bottom: 1.5rem;
            overflow: hidden;
        }
        
        .custom-progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #10b981, #06b6d4);
            border-radius: 999px;
            transition: width 0.4s ease;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        
        .status-success { background-color: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
        .status-warning { background-color: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
        .status-danger { background-color: #fff1f2; color: #be123c; border: 1px solid #fecdd3; }
        
        .content-text {
            font-size: 1.05rem;
            line-height: 1.7;
            color: #334155;
            margin-bottom: 1rem;
        }
        
        .content-text strong {
            color: #0f172a;
        }
        </style>
    """, unsafe_allow_html=True)

# Generate Mock Data Terlengkap
@st.cache_data
def get_mock_data():
    cabang_data = pd.DataFrame({
        'kode_cabang': ['CAB01', 'CAB02', 'CAB03', 'CAB04'],
        'nama_cabang': ['Kendari Utama', 'Mandonga', 'Wua-Wua', 'Unaaha'],
        'wilayah': ['Kendari Barat', 'Kendari Utara', 'Wua-Wua', 'Kab. Konawe'],
        'target_kredit': [25000000000, 15000000000, 18000000000, 10000000000],
        'realisasi_kredit': [26200000000, 14200000000, 17800000000, 10500000000]
    })
    
    ao_data = pd.DataFrame({
        'kode_ao': ['AO01', 'AO02', 'AO03', 'AO04', 'AO05'],
        'nama_ao': ['Andi Pratama', 'Siti Rahma', 'Budi Santoso', 'Dewi Lestari', 'Edi Wijaya'],
        'kode_cabang': ['CAB01', 'CAB01', 'CAB02', 'CAB03', 'CAB04'],
    })
    
    np.random.seed(42)
    n_nasabah = 100
    names = ['Mulyady Mustamin', 'Sri Wahyuni', 'Asrul Sani', 'Fitriani', 'Rian Hidayat', 
             'Harniati', 'La Ode Muhammad', 'Wa Ode Siti', 'Jumardin', 'Kusuma Wardani']
    sectors = ['Perdagangan Sembako', 'Pertanian Padi', 'Jasa Transportasi', 'Kios Kelontong', 
                'Kuliner / Warung Makan', 'Industri Rumah Tangga', 'Pegawai Swasta']
    
    nasabah_list, kredit_list, jaminan_list, angsuran_list = [], [], [], []
    
    for i in range(1, n_nasabah + 1):
        name_orig = names[i % len(names)] + f" {chr(65 + (i % 26))}"
        name_masked = name_orig[0] + ". " + "*" * 5
        
        plafon = int(np.random.choice([10, 25, 50, 100, 250, 500]) * 1000000)
        baki_debet = int(plafon * np.random.uniform(0.4, 0.95))
        kol = int(np.random.choice([1, 2, 3, 4, 5], p=[0.75, 0.15, 0.04, 0.03, 0.03]))
        tunggakan_hari = 0 if kol == 1 else (int(np.random.uniform(1, 30)) if kol == 2 else int(np.random.uniform(91, 270)))
        tunggakan_pokok = 0 if tunggakan_hari == 0 else int(baki_debet * np.random.uniform(0.02, 0.1))
        
        nasabah_list.append({
            'id_nasabah': f'NSB{i:04d}',
            'nama_asli': name_orig,
            'nama_masked': name_masked,
            'sektor_usaha': np.random.choice(sectors),
            'wilayah': np.random.choice(['Kendari', 'Konawe', 'Kolaka', 'Muna'])
        })
        
        kredit_list.append({
            'no_kredit': f'KRT{i:04d}',
            'id_nasabah': f'NSB{i:04d}',
            'kode_ao': np.random.choice(ao_data['kode_ao']),
            'plafon': plafon,
            'baki_debet': baki_debet,
            'kolektibilitas': kol,
            'tunggakan_hari': tunggakan_hari,
            'tunggakan_pokok': tunggakan_pokok,
            'status_restrukturisasi': np.random.choice(['Tidak', 'Ya'], p=[0.85, 0.15]),
            'tanggal_akad': (datetime.now() - timedelta(days=int(np.random.uniform(100, 800)))).strftime('%Y-%m-%d'),
            'tanggal_jatuh_tempo': (datetime.now() + timedelta(days=int(np.random.uniform(30, 800)))).strftime('%Y-%m-%d')
        })
        
        jaminan_list.append({
            'no_kredit': f'KRT{i:04d}',
            'jenis_agunan': np.random.choice(['SHM', 'BPKB Mobil', 'BPKB Motor', 'Deposito']),
            'nilai_agunan': int(plafon * np.random.uniform(1.2, 2.5))
        })
        
    nasabah_df = pd.DataFrame(nasabah_list)
    kredit_df = pd.DataFrame(kredit_list)
    jaminan_df = pd.DataFrame(jaminan_list)
    
    return cabang_data, ao_data, nasabah_df, kredit_df, jaminan_df

cabang_df, ao_df, nasabah_df, kredit_df, jaminan_df = get_mock_data()

# Progress state
if 'progress' not in st.session_state:
    st.session_state.progress = {
        'modul1': False, 'modul2': False, 'modul3': False, 'modul4': False,
        'modul5': False, 'modul6': False, 'modul7': False, 'modul8': False,
        'modul9': False, 'quiz_completed': False, 'quiz_score': 0
    }

completed_modules = sum([1 for k, v in st.session_state.progress.items() if k.startswith('modul') and v])
progress_percentage = int((completed_modules / 9) * 100)

def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <div style="background: linear-gradient(135deg, #10b981, #06b6d4); width: 64px; height: 64px; border-radius: 16px; display: grid; place-items: center; margin: 0 auto; color: white; font-weight: 800; font-size: 1.5rem;">
                    BI
                </div>
                <h3 style="margin-top: 1rem; margin-bottom: 0.2rem; font-weight: 800;">Finance BI Hub</h3>
                <p style="font-size: 0.8rem; color: #64748b; font-weight: 500;">Metabase, Dify & AI Guardrail</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        st.markdown(f"**Progres Belajar: {progress_percentage}%**")
        st.markdown(
            f"""
            <div class="custom-progress-container">
                <div class="custom-progress-bar" style="width: {progress_percentage}%;"></div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        modules = [
            ("1. Fondasi Finance BI", "modul1"),
            ("2. KPI & Pertanyaan Bisnis", "modul2"),
            ("3. Data Source & Semantic Layer", "modul3"),
            ("4. Dashboard Metabase", "modul4"),
            ("5. Data Quality & Reconciliation", "modul5"),
            ("6. Insight & Executive Summary", "modul6"),
            ("7. Dify Workflow BI Helper", "modul7"),
            ("8. AI Guardrail & Governance", "modul8"),
            ("9. Capstone Finance BI Hub", "modul9"),
        ]
        
        selection = st.radio("Materi Kursus:", [m[0] for m in modules], label_visibility="collapsed")
        
        st.markdown("---")
        if st.session_state.progress['quiz_completed']:
            st.markdown(
                f"<div class='status-badge status-success' style='width:100%; justify-content:center;'>🏆 Sertifikasi Selesai ({st.session_state.progress['quiz_score']}/10)</div>", 
                unsafe_allow_html=True
            )
        else:
            if st.button("📝 Ujian Sertifikasi AI BI", use_container_width=True):
                st.session_state.selected_quiz = True
                st.rerun()
                
    return selection

inject_custom_css()
selected_modul_name = render_sidebar()

if 'selected_quiz' in st.session_state and st.session_state.selected_quiz:
    st.markdown("<h1 class='gradient-text'>📝 Ujian Sertifikasi Finance BI Hub</h1>", unsafe_allow_html=True)
    st.markdown("<div class='content-text'>Uji pemahaman komprehensif Anda tentang Dashboard Metabase, Data Quality, dan AI Guardrail di sektor BPR.</div>", unsafe_allow_html=True)
    
    with st.form("quiz_form"):
        q1 = st.radio("1. Apa perbedaan utama antara Laporan biasa dengan Finance BI Hub?",
            ["Laporan hanya berisi tabel mati, Finance BI Hub adalah ekosistem (Dashboard, Validasi, AI) pendukung keputusan.", "Sama saja, hanya beda nama.", "BI Hub mencetak laporan secara fisik otomatis."])
        q2 = st.radio("2. Manakah urutan pendekatan BI yang benar?",
            ["Tarik semua data dari database -> Buat grafik -> Cari kesimpulan.", "Tentukan KPI dan Pertanyaan Bisnis -> Identifikasi Data Source -> Bangun Semantic Layer -> Dashboard."])
        q3 = st.radio("3. Jika outstanding naik 12% tetapi NPL naik dari 3.1% ke 4.8%, apa kesimpulan paling aman?",
            ["Kredit bertumbuh namun kualitas portofolio memburuk, butuh evaluasi kebijakan kolektibilitas.", "Kredit sukses besar dan cabang berhak dapat bonus."])
        q4 = st.radio("4. Jika data dashboard berbeda dengan laporan Core Banking, apa langkah pertama?",
            ["Langsung salahkan IT dan matikan server.", "Lakukan proses Rekonsiliasi, cek tanggal update terakhir (Data Quality log), dan identifikasi data missing."])
        q5 = st.radio("5. Mengapa Dify / AI Helper TIDAK BOLEH diberi akses INSERT atau UPDATE ke database?",
            ["Karena AI bisa merusak, memanipulasi, atau menghapus data transaksi (destruktif). Akses AI wajib READ-ONLY.", "Boleh saja agar AI bisa membetulkan data yang salah secara otomatis."])
        q6 = st.radio("6. Apakah AI boleh menyimpulkan cabang melakukan fraud (kecurangan) hanya karena NPL naik?",
            ["Ya, NPL naik selalu berarti ada fraud.", "Tidak boleh. AI tidak boleh membuat tuduhan atau asumsi tanpa bukti data forensik yang jelas."])
        q7 = st.radio("7. Query SQL apa yang HARUS DIBLOKIR untuk AI Assistant di lingkungan Finance?",
            ["SELECT, JOIN, WHERE", "UPDATE, DELETE, DROP, TRUNCATE, ALTER"])
        q8 = st.radio("8. Mengapa data nasabah harus dimasking (dianonimkan)?",
            ["Agar nama nasabah terlihat lebih keren.", "Menghindari kebocoran data pribadi (UU PDP / GDPR) jika dashboard diakses banyak pihak."])
        q9 = st.radio("9. Apa peran utama Metabase dalam arsitektur ini?",
            ["Menyimpan data mentah.", "Sebagai Dashboard Utama dan visualisasi (Operational & Executive Dashboard) yang interaktif."])
        q10 = st.radio("10. Apa yang harus ada dalam Executive Summary yang baik?",
            ["Puluhan halaman tabel raw data.", "Temuan, Bukti Angka, Dampak, Rekomendasi, dan Catatan Validasi Data."])
        
        if st.form_submit_button("Kirim Jawaban Sertifikasi", type="primary"):
            score = sum([
                1 if "ekosistem" in q1 else 0,
                1 if "Tentukan KPI" in q2 else 0,
                1 if "kualitas portofolio memburuk" in q3 else 0,
                1 if "Rekonsiliasi" in q4 else 0,
                1 if "destruktif" in q5 else 0,
                1 if "Tidak boleh" in q6 else 0,
                1 if "UPDATE, DELETE" in q7 else 0,
                1 if "kebocoran data" in q8 else 0,
                1 if "Dashboard Utama" in q9 else 0,
                1 if "Temuan, Bukti" in q10 else 0
            ])
            st.session_state.progress['quiz_completed'] = True
            st.session_state.progress['quiz_score'] = score
            st.success(f"Skor Anda: {score}/10")
            
    if st.button("Kembali ke Modul Belajar"):
        st.session_state.selected_quiz = False
        st.rerun()

else:
    # MODUL 1
    if selected_modul_name.startswith("1."):
        st.session_state.progress['modul1'] = True
        st.markdown("<h1 class='gradient-text'>🚀 Modul 1: Fondasi Finance BI</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Tujuan:</b> Memahami bahwa Business Intelligence (BI) di sektor BPR/BPRS bukan sekadar membuat grafik visual, melainkan sebuah ekosistem utuh pendukung keputusan bisnis.<br><br>
            <b>Dari Data Menjadi Keputusan:</b><br>
            <ul>
                <li><i>Data Mentah:</i> Daftar kredit bulan ini (ratusan baris excel).</li>
                <li><i>Informasi/Dashboard:</i> Grafik tren kredit dan rasio kolektibilitas per cabang.</li>
                <li><i>Insight:</i> "Kredit cabang A tumbuh pesat, namun kualitas pembayarannya terus menurun."</li>
                <li><i>Keputusan:</i> Lakukan audit lapangan di Cabang A dan tunda persetujuan plafon baru.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏛️ Mengapa BPR Membutuhkan BI Hub?")
        st.markdown("""
        <div class='glass-card content-text'>
            Keputusan strategis direksi tidak boleh berbasis intuisi. <b>Finance BI Hub</b> menyatukan seluruh aliran data—mulai dari Core Banking, Semantic Layer, Dashboard Metabase, hingga Dify AI Assistant—agar manajemen mendapatkan informasi yang valid, aman, dan dapat dipertanggungjawabkan (auditable).
        </div>
        """, unsafe_allow_html=True)

    # MODUL 2
    elif selected_modul_name.startswith("2."):
        st.session_state.progress['modul2'] = True
        st.markdown("<h1 class='gradient-text'>🎯 Modul 2: KPI & Pertanyaan Bisnis</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Prinsip Utama BI:</b> Jangan mulai dari mencari data, mulailah dari menentukan **Pertanyaan Bisnis** dan **KPI (Key Performance Indicator)** yang ingin dijawab.<br><br>
            <b>KPI Kritis BPR/BPRS:</b>
            <ul>
                <li><b>Outstanding Kredit:</b> Sisa pokok pinjaman berjalan.</li>
                <li><b>NPL (Non-Performing Loan):</b> Rasio kredit macet (Kol 3, 4, 5) terhadap total kredit.</li>
                <li><b>DPK (Dana Pihak Ketiga):</b> Jumlah tabungan & deposito nasabah.</li>
                <li><b>Kolektibilitas:</b> 1 (Lancar) hingga 5 (Macet).</li>
            </ul>
            <br>
            <b>Pertanyaan Bisnis yang Harus Dijawab Dashboard:</b>
            <i>"Cabang mana yang paling sehat?", "Sektor usaha apa yang mulai memburuk?", "Apakah pertumbuhan kredit sejalan dengan kualitas pembayarannya?"</i>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎮 Simulator Risiko NPL")
        st.write("Ubah nilai di bawah untuk melihat perhitungan NPL secara live.")
        kol_lancar = st.slider("Kredit Lancar (Kol 1-2) Juta Rp", 1000, 10000, 8000)
        kol_macet = st.slider("Kredit Macet (Kol 3-5) Juta Rp", 0, 1500, 100)
        
        total = kol_lancar + kol_macet
        npl = (kol_macet / total) * 100
        
        st.metric("Total Outstanding", f"Rp {total} Juta")
        st.metric("Rasio NPL", f"{npl:.2f}%")
        if npl > 5:
            st.error("🚨 PERINGATAN: Rasio NPL di atas batas toleransi 5%.")
            st.markdown("""
            <div style='background-color: #fff1f2; padding: 1rem; border-radius: 8px; border-left: 4px solid #be123c; margin-top: 0.5rem;'>
                <b>Mengapa ini berbahaya?</b><br>
                <ul style='margin-bottom: 0;'>
                    <li><b>Regulasi OJK:</b> Batas maksimal NPL (Non-Performing Loan) yang dianggap sehat oleh Otoritas Jasa Keuangan (OJK) adalah 5%. Melewati batas ini BPR dapat dikenakan sanksi atau pengawasan intensif.</li>
                    <li><b>Beban Modal (CKPN):</b> Semakin tinggi NPL, Bank wajib mencadangkan lebih banyak dana untuk risiko kerugian (CKPN), yang akan langsung memotong laba bersih bank.</li>
                    <li><b>Likuiditas:</b> Dana macet berarti arus kas masuk terhenti, mengganggu kemampuan bank untuk memutar dana (menyalurkan kredit baru atau membayar bunga deposan).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("✅ AMAN: NPL terjaga dengan baik.")

    # MODUL 3
    elif selected_modul_name.startswith("3."):
        st.session_state.progress['modul3'] = True
        st.markdown("<h1 class='gradient-text'>🗂️ Modul 3: Data Source & Semantic Layer</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Tujuan:</b> Mengetahui data apa saja yang perlu ditarik dari Core Banking ke Finance Data Mart untuk membentuk Semantic Layer.<br><br>
            <b>Struktur Data Utama (Entity):</b>
            <ul>
                <li>Data Kredit (Plafon, Baki Debet, Tunggakan Hari, Status Restrukturisasi)</li>
                <li>Data Nasabah (Profil anonim, Sektor Usaha, Wilayah)</li>
                <li>Data Jaminan/Agunan (Jenis, Nilai Pasar)</li>
            </ul>
            <b>Semantic Layer (SQL View):</b> adalah lapisan yang mengubah raw data menjadi tabel rapi yang siap dibaca oleh Metabase dan AI, sehingga formula KPI seragam di seluruh bank.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔍 Masking Data Nasabah (Simulasi)")
        st.write("Data sensitif nasabah WAJIB disamarkan (masking) demi kepatuhan regulasi privasi data.")
        if st.checkbox("Aktifkan Masking (Aman)"):
            st.dataframe(nasabah_df.drop(columns=['nama_asli']))
        else:
            st.warning("⚠️ Menampilkan data asli berpotensi melanggar UU Pelindungan Data Pribadi (PDP).")
            st.markdown("""
            <div style='background-color: #fffbeb; padding: 1rem; border-radius: 8px; border-left: 4px solid #b45309; margin-top: 0.5rem; margin-bottom: 1rem;'>
                <b>Mengapa Pelanggaran Privasi Berbahaya?</b><br>
                <ul style='margin-bottom: 0;'>
                    <li><b>Sanksi UU PDP:</b> Membuka data pribadi tanpa izin / enkripsi dapat berakibat sanksi denda miliaran rupiah menurut Undang-Undang Pelindungan Data Pribadi.</li>
                    <li><b>Risiko Reputasi:</b> Hilangnya kepercayaan nasabah (risiko rush money) jika data mereka bocor dan digunakan untuk penipuan (phishing/social engineering).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(nasabah_df.drop(columns=['nama_masked']))

    # MODUL 4
    elif selected_modul_name.startswith("4."):
        st.session_state.progress['modul4'] = True
        st.markdown("<h1 class='gradient-text'>📊 Modul 4: Dashboard Metabase</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Mengapa Metabase, bukan Excel?</b><br>
            Excel memang fleksibel, tapi memiliki risiko fatal untuk level institusi: sangat rentan <i>human-error</i> (salah rumus/copy-paste), versi file yang berantakan (Laporan_Final_Revisi3.xlsx), dan berisiko tinggi terhadap keamanan data karena sangat mudah disalin ke flashdisk pribadi. Metabase menyelesaikan ini dengan koneksi langsung ke database secara terpusat, real-time (satu sumber kebenaran), dan dengan manajemen hak akses yang ketat.<br><br>
            <b>Rancangan Dashboard Produksi BPR:</b>
            <ul>
                <li><b>Executive Overview:</b> Ringkasan untuk Direksi (Laba, Total Aset, NPL Gross).</li>
                <li><b>Credit Portfolio:</b> Persebaran kredit per sektor usaha dan wilayah.</li>
                <li><b>Branch & AO Performance:</b> Membandingkan realisasi vs target tiap cabang/Account Officer.</li>
                <li><b>Collection Dashboard:</b> Pemantauan debitur yang mendekati jatuh tempo dan status tunggakan.</li>
            </ul>
            <br>
            <i>(Di kelas ini, kita menggunakan Streamlit sebagai sarana simulasi pembelajaran dari dashboard Metabase tersebut.)</i>
        </div>
        """, unsafe_allow_html=True)

    # MODUL 5
    elif selected_modul_name.startswith("5."):
        st.session_state.progress['modul5'] = True
        st.markdown("<h1 class='gradient-text'>🛡️ Modul 5: Data Quality & Reconciliation</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Tujuan:</b> Memastikan angka di dashboard benar-benar valid dan sama dengan laporan Core Banking / Akuntansi.<br><br>
            <div style='background-color: #fff1f2; padding: 1rem; border-radius: 8px; border-left: 4px solid #be123c; margin-bottom: 1rem;'>
                <b>Bahaya Membersihkan Data Secara Sepihak:</b><br>
                Jika Anda menemukan data plafon minus dan langsung mengubahnya menjadi positif di layer Dashboard (tanpa memberitahu IT/Core Banking), maka angka Dashboard akan "terlihat" benar, tetapi <b>Buku Besar Akuntansi tetap salah</b>. Ini akan menjadi temuan fatal saat diaudit oleh KAP atau OJK karena adanya selisih antara sistem utama dan laporan manajemen!
            </div>
            <b>Praktik yang Benar (Finance Grade):</b>
            <ul>
                <li>Lakukan <b>Rekonsiliasi</b> antara total Outstanding Dashboard vs Buku Besar Akuntansi.</li>
                <li>Lacak anomali (contoh: Nilai plafon minus, tanggal jatuh tempo di masa lalu).</li>
                <li>Tampilkan <i>Data Quality Score</i> dan tanggal pembaruan (last sync) secara transparan di dashboard.</li>
                <li>Laporkan error ke tim Core Banking untuk dikoreksi pada sumbernya.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # MODUL 6
    elif selected_modul_name.startswith("6."):
        st.session_state.progress['modul6'] = True
        st.markdown("<h1 class='gradient-text'>📝 Modul 6: Insight & Executive Summary</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Dari Angka Menjadi Narasi:</b> Manajemen tingkat atas membutuhkan Executive Summary yang memadatkan puluhan grafik menjadi 1 halaman keputusan.<br><br>
            <b>Pola Narasi Insight yang Tepat:</b>
            <ol>
                <li><b>Temuan:</b> Apa yang berubah?</li>
                <li><b>Bukti Angka:</b> Naik/turun seberapa besar? Berasal dari cabang mana?</li>
                <li><b>Dampak & Risiko:</b> Apa risikonya jika dibiarkan?</li>
                <li><b>Rekomendasi:</b> Apa yang harus dilakukan operasional/direksi?</li>
                <li><b>Catatan Validasi:</b> Sumber data dan status rekonsiliasi.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### 🤖 Generator Executive Summary")
        topik = st.selectbox("Pilih Topik", ["Laporan Kualitas Kredit", "Laporan Pertumbuhan DPK"])
        if st.button("Generate Template Summary"):
            st.info(f"**{topik}**\n\n**Temuan:** Terdapat anomali pada rasio pertumbuhan.\n**Bukti Angka:** Outstanding tumbuh 12% namun NPL menembus 4.5% di Cabang Mandonga.\n**Rekomendasi:** Lakukan audit lapangan pada portofolio Cabang Mandonga bulan ini.\n**Status Validasi:** Data tersinkronisasi 100% dengan Core Banking.")
            st.markdown("""
            <div style='background-color: #eff6ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #1d4ed8; margin-top: 1rem;'>
                <b>Mengapa format ini wajib dipatuhi?</b><br>
                Direksi BPR tidak punya waktu menelusuri ratusan baris tabel untuk mencari tahu apa yang salah. Mereka hanya punya waktu 2 menit untuk membaca kesimpulan dan bertindak. Jika BI Hub gagal menyajikan <b>Bukti Angka</b> dan <b>Rekomendasi Aksi</b> secara spesifik, maka dashboard secanggih apapun menjadi tidak berguna karena gagal memicu keputusan bisnis.
            </div>
            """, unsafe_allow_html=True)

    # MODUL 7
    elif selected_modul_name.startswith("7."):
        st.session_state.progress['modul7'] = True
        st.markdown("<h1 class='gradient-text'>⚙️ Modul 7: Dify Workflow BI Helper</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Apa itu Dify?</b> Dify adalah platform untuk mengorkestrasi alur kerja (workflow) Artificial Intelligence. Dalam Finance BI, Dify menjadi "otak" di belakang AI BI Helper.<br><br>
            <b>Alur Kerja (Workflow) Dify:</b>
            <ol>
                <li>User memilih filter dashboard (contoh: Cabang Unaaha, NPL > 3%).</li>
                <li>Dify menarik metadata angka tersebut dengan mode <i>Read-Only</i>.</li>
                <li>Dify mencocokkan angka dengan <b>Knowledge Base</b> (SOP Bank, Aturan Kolektibilitas OJK).</li>
                <li><i>Validation Agent</i> memeriksa apakah AI berhalusinasi atau angkanya melenceng.</li>
                <li>Dify menghasilkan draft analisa dalam format <i>Executive Summary</i> untuk dibaca manusia.</li>
            </ol>
            <div style='background-color: #fffbeb; padding: 1rem; border-radius: 8px; border-left: 4px solid #b45309; margin-top: 1rem;'>
                <b>Mengapa tidak pakai ChatGPT biasa saja?</b><br>
                Mengunggah data finansial/nasabah ke ChatGPT publik adalah pelanggaran kepatuhan tingkat tinggi (membocorkan rahasia bank). Selain itu, ChatGPT publik tidak mengetahui SOP internal Bank Anda, tidak tahu rumus KPI spesifik perusahaan, dan sangat rentan berhalusinasi (mengarang angka). Dify menyelesaikan ini dengan menjalankan AI secara privat dan mengunci sumber informasinya hanya dari <i>Knowledge Base</i> milik perusahaan.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # MODUL 8
    elif selected_modul_name.startswith("8."):
        st.session_state.progress['modul8'] = True
        st.markdown("<h1 class='gradient-text'>🚦 Modul 8: AI Guardrail & Governance</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Keamanan Tingkat Tinggi (Anti-Destruktif & Anti-Halusinasi):</b><br>
            Di sektor perbankan, AI tidak boleh mengambil keputusan final dan tidak boleh merusak data transaksi.<br><br>
            <b>Aturan Ketat (Guardrails) untuk AI:</b>
            <ul>
                <li><b>No Write Access:</b> AI dilarang keras menjalankan query destruktif (`UPDATE`, `DELETE`, `DROP`, `INSERT`). 
                <div style='background-color: #fff1f2; padding: 0.8rem; border-radius: 8px; border-left: 4px solid #be123c; margin-top: 0.5rem; margin-bottom: 0.5rem; color: #334155;'>
                    <b>Risiko Fatal:</b> Jika AI diberikan koneksi bebas, sebuah kalimat prompt sederhana seperti <i>"tolong hapus kredit yang sudah lunas"</i> bisa membuat AI mengeksekusi <code>DELETE FROM tabel_kredit</code> tanpa filter. Seluruh data bank lenyap seketika! Koneksi AI ke database <b>WAJIB Read-Only</b>.
                </div>
                </li>
                <li><b>No Fraud Accusation:</b> AI dilarang menuduh cabang/AO melakukan <i>fraud</i> tanpa bukti forensik numerik yang konkret.</li>
                <li><b>Transparency:</b> AI wajib mengutip darimana angka tersebut berasal. Jika data kosong, AI wajib menjawab: <i>"Data tidak cukup untuk menyimpulkan."</i> (Bukan mengarang angka/halusinasi).</li>
                <li><b>Human-in-the-loop:</b> Rekomendasi restrukturisasi/penolakan kredit dari AI hanya berstatus draf. Keputusan eksekusi 100% wajib disetujui manusia.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # MODUL 9
    elif selected_modul_name.startswith("9."):
        st.session_state.progress['modul9'] = True
        st.markdown("<h1 class='gradient-text'>🏆 Modul 9: Capstone Finance BI Hub</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='glass-card content-text'>
            <b>Tugas Akhir Implementasi:</b><br>
            Peserta diharapkan dapat menyusun blueprint (cetak biru) pembangunan Finance BI Hub di bank masing-masing. Output blueprint harus mencakup:
            <ol>
                <li>Daftar KPI dan Definisi Rumus (Data Dictionary).</li>
                <li>Desain Dashboard Utama di Metabase.</li>
                <li>Checklist Validasi Kualitas Data.</li>
                <li>Matriks Hak Akses (Role-based access) dari Direktur hingga staf.</li>
                <li>Skenario pengamanan dan pembatasan wewenang AI (AI Guardrail).</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 Preview Blueprint Dashboard BPR")
        c1, c2, c3 = st.columns(3)
        c1.metric("Plafon Penyaluran", "Rp 68.00 M", "Target Tercapai")
        c2.metric("NPL Net BPR", "3.24%", "Stabil")
        c3.metric("Data Quality Score", "98.5%", "Tervalidasi")
        
        st.write("Grafik Realisasi Kredit per Cabang")
        st.bar_chart(cabang_df.set_index('nama_cabang')[['realisasi_kredit']])
