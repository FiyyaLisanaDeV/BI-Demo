import streamlit as st
import os
import subprocess
from src.utils import check_password

st.set_page_config(page_title="Administrator Panel", layout="wide", page_icon="⚙️")

if not check_password():
    st.stop()

# --- Admin Authentication Logic ---
if 'admin_unlocked' not in st.session_state:
    st.session_state.admin_unlocked = False

if not st.session_state.admin_unlocked:
    st.markdown("### 🔐 Otorisasi Super Admin Diperlukan")
    st.info("Halaman ini berisi instrumen kontrol infrastruktur (*backend*). Hanya diperuntukkan bagi tim IT / SysAdmin.")
    pin = st.text_input("Masukkan PIN Administrator (Hint: 1234)", type="password")
    if st.button("Buka Kunci Panel"):
        if pin == "1234":
            st.session_state.admin_unlocked = True
            st.rerun()
        else:
            st.error("PIN Salah!")
    st.stop()

# --- Admin Dashboard Content ---
st.title("⚙️ System Administrator Panel")
st.markdown("Pusat kendali untuk manajemen infrastruktur server, monitoring log, dan eksekusi *Data Pipeline* Finance BI.")
st.markdown("---")

# 1. System Diagnostics
st.header("1. 🖥️ Diagnostik Server & Infrastruktur")
col1, col2, col3, col4 = st.columns(4)

def get_system_metrics():
    try:
        mem = subprocess.check_output("free -m | awk '/Mem:/ {print $3/$2 * 100.0}'", shell=True).decode('utf-8').strip()
        disk = subprocess.check_output("df -h / | awk 'NR==2 {print $5}'", shell=True).decode('utf-8').strip()
        uptime = subprocess.check_output("uptime -p", shell=True).decode('utf-8').strip()
        return mem, disk, uptime
    except:
        return "0", "0%", "Unknown"

mem, disk, uptime = get_system_metrics()
col1.metric("Memory (RAM) Usage", f"{float(mem):.1f}%" if mem else "N/A")
col2.metric("Storage (Disk) Used", disk if disk else "N/A")
col3.metric("Server Uptime", uptime.replace('up ', '') if uptime else "N/A")
col4.metric("Nginx Proxy", "Active (Port 80/443)")

st.markdown("<br>", unsafe_allow_html=True)

# 2. ETL Pipeline Controller
st.header("2. 🔄 Pengendali Data Pipeline (ETL)")
st.info("Gunakan modul ini untuk melakukan *reset* atau memperbarui seluruh data simulasi secara manual. Hal ini berguna untuk demonstrasi *real-time streaming* data baru.")

c1, c2 = st.columns(2)
with c1:
    st.subheader("📦 Bronze Layer (Raw Data Generator)")
    st.write("Jalankan modul generator untuk membuat 3.000 entitas nasabah baru beserta riwayat transaksi acak (File `.xlsx`). Data lama akan ditimpa.")
    if st.button("🚀 Generate New Raw Data", use_container_width=True, type="primary"):
        with st.spinner("Menghasilkan data mentah baru... (Membutuhkan waktu ~30 detik)"):
            try:
                env = os.environ.copy()
                env['PYTHONPATH'] = '/root/finance-bi-course'
                res = subprocess.run(["/root/finance-bi-course/.venv/bin/python3", "scripts/generate_dummy_data.py"], capture_output=True, text=True, cwd='/root/finance-bi-course', env=env)
                if res.returncode == 0:
                    st.success("✅ Berhasil membuat data mentah (Raw Data) baru di `data/raw/`!")
                else:
                    st.error(f"Gagal: {res.stderr}")
            except Exception as e:
                st.error(f"Error executing script: {e}")

with c2:
    st.subheader("🏆 Gold Layer (Data Mart Transformer)")
    st.write("Jalankan *pipeline ETL* untuk mengekstrak, memvalidasi, dan mengagregasi data mentah menjadi bentuk *Data Mart* yang siap disajikan ke dasbor.")
    if st.button("⚡ Run ETL & Data Masking", use_container_width=True, type="primary"):
        with st.spinner("Memproses transformasi data dan menerapkan regulasi POJK (Data Masking)..."):
            try:
                env = os.environ.copy()
                env['PYTHONPATH'] = '/root/finance-bi-course'
                res = subprocess.run(["/root/finance-bi-course/.venv/bin/python3", "scripts/transform_to_mart.py"], capture_output=True, text=True, cwd='/root/finance-bi-course', env=env)
                if res.returncode == 0:
                    st.success("✅ Data Mart berhasil diperbarui! Dasbor kini menyajikan informasi dari *pipeline* terbaru.")
                else:
                    st.error(f"Gagal: {res.stderr}")
            except Exception as e:
                st.error(f"Error executing script: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# 3. Service Manager
st.header("3. 🔧 Manajemen Servis (Systemd)")
st.write("Fitur ini memungkinkan administrator me-restart antarmuka *web server* tanpa harus masuk ke terminal SSH. Sangat berguna ketika terjadi masalah *cache* pada *browser*.")
if st.button("🔁 Restart Web Server (Streamlit)", type="secondary"):
    try:
        # We start it asynchronously because restarting the current process will kill this request!
        subprocess.Popen("sleep 2 && systemctl restart finance-bi-course.service", shell=True)
        st.warning("⚠️ Perintah Restart telah dikirim! Aplikasi akan termuat ulang (reload) dalam 3 detik. Harap tunggu...")
    except Exception as e:
        st.error(f"Gagal me-restart servis: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# 4. Live Logs
st.header("4. 📋 Live Server Logs (Streamlit Service)")
st.write("Pantau aktivitas sistem (*error/warnings/access*) secara langsung (Membaca 50 baris terakhir dari *journalctl*).")

if st.button("🔄 Segarkan Log (Refresh Logs)"):
    pass

try:
    logs = subprocess.check_output(["journalctl", "-u", "finance-bi-course.service", "-n", "50", "--no-pager"]).decode('utf-8')
    st.code(logs, language="bash")
except Exception as e:
    st.error("Gagal membaca log sistem.")
