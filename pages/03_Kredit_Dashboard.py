import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="Kredit Dashboard", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("Kredit Dashboard")

df_loans = load_mart("mart_loans")

if df_loans.empty:
    st.warning("Data not available.")
else:
    # Filters
    st.sidebar.header("Filter")
    sectors = df_loans['economic_sector'].unique() if 'economic_sector' in df_loans.columns else []
    selected_sector = st.sidebar.multiselect("Sektor Ekonomi", sectors, default=sectors)
    
    df_filtered = df_loans[df_loans['economic_sector'].isin(selected_sector)] if 'economic_sector' in df_loans.columns else df_loans
    
    render_summary(df_filtered, "kredit")
    col1, col2, col3 = st.columns(3)
    tot_plafond = df_filtered['principal_amount'].sum()
    tot_out = df_filtered['outstanding_principal'].sum()
    
    col1.metric("Total Plafond", f"Rp {tot_plafond:,.2f}")
    col2.metric("Total Outstanding", f"Rp {tot_out:,.2f}")
    col3.metric("Jumlah Fasilitas", f"{len(df_filtered)}")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Kredit per Produk")
        fig1 = px.bar(df_filtered.groupby('loan_product')['outstanding_principal'].sum().reset_index(), x='loan_product', y='outstanding_principal')
        st.plotly_chart(fig1, width='stretch')
    with c2:
        st.subheader("Kredit per Sektor Ekonomi")
        if 'economic_sector' in df_filtered.columns:
            fig2 = px.pie(df_filtered, names='economic_sector', values='outstanding_principal')
            st.plotly_chart(fig2, width='stretch')
            
    st.markdown("---")
    st.subheader("Data Kredit")
    st.dataframe(df_filtered.head(100))
    apply_download_button(df_filtered, "kredit_data.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan Portofolio Kredit:**
    - **Baki Debet (Outstanding):** Nilai pokok pinjaman yang belum dilunasi oleh debitur (`Principal - Total Angsuran Pokok Masuk`).
    - **Rata-rata Suku Bunga:** Dihitung menggunakan rata-rata aritmatika dari nominal suku bunga per tahun (*Annualized Interest Rate*) pada rekening aktif.
    """)
