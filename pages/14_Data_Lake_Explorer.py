import streamlit as st
import pandas as pd
import os
import glob
from pathlib import Path
from src.utils import apply_download_button, check_password

st.set_page_config(page_title="Data Lake Explorer", layout="wide")

if not check_password():
    st.stop()

st.title("🌊 Data Lake Explorer")
st.markdown("Akses seluruh repository data mentah, data bersih (mart), dan data tertolak (rejected) langsung dari satu tempat.")

# Tentukan root path dari direktori data
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

if not os.path.exists(data_dir):
    st.error(f"Direktori data tidak ditemukan di: {data_dir}")
    st.stop()

# Deteksi subfolder dalam direktori data
subfolders = [f.name for f in os.scandir(data_dir) if f.is_dir()]
subfolders.sort()

if not subfolders:
    st.warning("Belum ada subdirektori di dalam folder data.")
    st.stop()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📂 Navigasi Direktori")
    selected_folder = st.selectbox("Pilih Layer Data", subfolders, help="Pilih layer data (raw, mart, rejected)")
    
    folder_path = os.path.join(data_dir, selected_folder)
    
    # Cari semua file data yang didukung di folder tersebut
    file_patterns = ["*.csv", "*.xlsx", "*.xls", "*.parquet", "*.json"]
    files = []
    for ext in file_patterns:
        files.extend(glob.glob(os.path.join(folder_path, ext)))
    
    files.sort()
    file_names = [os.path.basename(f) for f in files]
    
    if not file_names:
        st.info(f"Tidak ada file data di dalam folder `{selected_folder}`.")
        selected_file = None
    else:
        selected_file = st.selectbox("Pilih Dataset", file_names)

with col2:
    st.subheader("📄 Preview Dataset")
    if file_names and selected_file:
        file_path = os.path.join(folder_path, selected_file)
        file_size_kb = os.path.getsize(file_path) / 1024
        
        st.markdown(f"**Path:** `data/{selected_folder}/{selected_file}`")
        st.markdown(f"**Ukuran File:** `{file_size_kb:.2f} KB`")
        
        try:
            # Batasi jumlah baris yang dibaca untuk file besar (preview)
            with st.spinner('Membaca data...'):
                if selected_file.endswith('.csv'):
                    df = pd.read_csv(file_path, nrows=1000)
                elif selected_file.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file_path, nrows=1000)
                elif selected_file.endswith('.parquet'):
                    df = pd.read_parquet(file_path)
                    if len(df) > 1000:
                        df = df.head(1000)
                elif selected_file.endswith('.json'):
                    df = pd.read_json(file_path)
                    if len(df) > 1000:
                        df = df.head(1000)
                else:
                    df = None
            
            if df is not None:
                st.dataframe(df, use_container_width=True)
                
                col_dl, col_info = st.columns([1, 3])
                with col_dl:
                    # Provide original file for download instead of just preview df
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                    
                    st.download_button(
                        label=f"⬇️ Download {selected_file}",
                        data=file_bytes,
                        file_name=selected_file,
                        mime="application/octet-stream"
                    )
                with col_info:
                    st.caption("Preview dibatasi maksimum 1000 baris. Download untuk melihat file utuh.")
            else:
                st.warning("Format file tidak didukung untuk preview.")
                
        except Exception as e:
            st.error(f"Gagal membaca file: {e}")

st.markdown("---")
with st.expander("ℹ️ Struktur Layer Data (Data Lake)"):
    st.markdown("""
    Sistem ini memisahkan data ke dalam tiga layer utama:
    - **`raw` (Raw Layer):** Data mentah yang masuk ke sistem, belum divalidasi atau dibersihkan. Sering kali mengandung duplikat atau kolom yang salah format.
    - **`rejected` (Quarantine Layer):** Data yang gagal melewati proses validasi kualitas data (Data Quality).
    - **`mart` (Data Mart Layer):** Data yang sudah dibersihkan, diagregasi, dan siap untuk divisualisasikan oleh dashboard.
    """)
