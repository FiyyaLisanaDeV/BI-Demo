import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.utils import apply_download_button
from src.summarizer import render_summary

st.set_page_config(page_title="KPI Kinerja SDM", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("👥 Dashboard Kinerja SDM & Pencapaian Target")

df_kpi = load_mart("mart_kpi_sdm")

if df_kpi.empty:
    st.warning("Data KPI SDM belum tersedia. Silakan jalankan proses transformasi data.")
else:
    # Adding a specific summary context for KPI if it's not present in summarizer
    # We can inject our own dynamic summary text here directly
    tot_emp = len(df_kpi)
    avg_ach = df_kpi['achievement_percentage'].mean()
    top_ao = df_kpi.loc[df_kpi['achievement_percentage'].idxmax()]['full_name'] if not df_kpi.empty else "N/A"
    
    st.info(f"💡 **Ringkasan Kinerja SDM:** Terdapat total **{tot_emp}** pegawai dalam data ini. Rata-rata persentase pencapaian target penyaluran kredit (KPI) di seluruh perusahaan berada di level **{avg_ach:.1f}%**. Account Officer dengan performa pencapaian tertinggi saat ini adalah **{top_ao}**.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pegawai", f"{tot_emp} Orang")
    col2.metric("Rata-rata Pencapaian KPI", f"{avg_ach:.2f}%")
    
    # Filter by Division/Department
    departments = df_kpi['department'].unique()
    selected_dept = st.sidebar.multiselect("Filter Departemen", departments, default=departments)
    df_filtered = df_kpi[df_kpi['department'].isin(selected_dept)]
    
    st.markdown("### Analisis Pencapaian Target (KPI) per Divisi/Pegawai")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Rata-rata Pencapaian per Jabatan")
        avg_pos = df_filtered.groupby('position')['achievement_percentage'].mean().reset_index()
        fig1 = px.bar(avg_pos, x='position', y='achievement_percentage', color='achievement_percentage',
                      color_continuous_scale='Viridis', title="Rata-Rata KPI per Jabatan (%)")
        st.plotly_chart(fig1, width='stretch')
        
    with c2:
        st.subheader("Pencapaian Tertinggi per Pegawai (Top 10)")
        top_10 = df_filtered.sort_values('achievement_percentage', ascending=False).head(10)
        fig2 = px.bar(top_10, x='full_name', y='achievement_percentage', color='department',
                      title="Top 10 Pegawai Berdasarkan KPI (%)")
        st.plotly_chart(fig2, width='stretch')
        
    st.markdown("---")
    st.subheader("Tabel Detil Kinerja Pegawai")
    display_cols = ['employee_id', 'full_name', 'department', 'position', 'total_loan_portfolio', 'kpi_target', 'achievement_percentage']
    
    # Format the dataframe for display
    df_display = df_filtered[display_cols].copy()
    df_display['total_loan_portfolio'] = df_display['total_loan_portfolio'].apply(lambda x: f"Rp {x:,.2f}")
    df_display['kpi_target'] = df_display['kpi_target'].apply(lambda x: f"Rp {x:,.2f}")
    df_display['achievement_percentage'] = df_display['achievement_percentage'].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(df_display, use_container_width=True)
    apply_download_button(df_filtered, "sdm_kpi_data.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan KPI SDM (Kinerja Penyaluran Kredit):**
    - **Total Portofolio Pinjaman (Realisasi):** `Σ Baki Debet (Outstanding Principal)` fasilitas kredit berstatus *Active* yang diprakarsai oleh *Account Officer* terkait.
    - **Target KPI:** Nominal absolut target penyaluran kredit. (Simulasi: Manajer = Rp 500.000.000, Staf = Rp 150.000.000).
    - **Persentase Pencapaian (Achievement Rate):** `(Realisasi Portofolio / Target KPI) × 100%`.
    """)
