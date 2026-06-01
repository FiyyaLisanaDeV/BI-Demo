import streamlit as st
import plotly.express as px
from src.loader import load_mart
from src.summarizer import render_summary
from src.utils import apply_download_button

st.set_page_config(page_title="GL & Accounting", layout="wide")

from src.utils import check_password
if not check_password():
    st.stop()

st.title("GL & Accounting Validation")

df_gl = load_mart("mart_gl")

if df_gl.empty:
    st.warning("Data not available.")
else:
    render_summary(df_gl, "gl")
    col1, col2, col3 = st.columns(3)
    tot_deb = df_gl['debit_amount'].sum()
    tot_cred = df_gl['credit_amount'].sum()
    diff = abs(tot_deb - tot_cred)
    
    col1.metric("Total Debit", f"Rp {tot_deb:,.2f}")
    col2.metric("Total Credit", f"Rp {tot_cred:,.2f}")
    col3.metric("Selisih", f"Rp {diff:,.2f}", delta_color="inverse" if diff > 0 else "off")
    
    if diff > 0.01:
        st.error("⚠️ Peringatan: Terdapat jurnal tidak balance secara keseluruhan!")
    else:
        st.success("✅ Seluruh Jurnal Balance")
        
    st.markdown("---")
    st.subheader("Trial Balance Sederhana")
    tb = df_gl.groupby(['gl_account_id', 'gl_name'])[['debit_amount', 'credit_amount']].sum().reset_index()
    tb['mutasi'] = tb['debit_amount'] - tb['credit_amount']
    st.dataframe(tb)
    apply_download_button(tb, "trial_balance.csv")

st.markdown("--- ")
with st.expander("ℹ️ Metodologi & Formulasi Perhitungan"):
    st.markdown("""
    **Standar Perhitungan Buku Besar (General Ledger):**
    - **Prinsip Double-Entry:** Setiap transaksi wajib mencatatkan nominal pada sisi Debit dan Kredit secara simultan.
    - **Persamaan Keseimbangan:** `Σ Debit - Σ Kredit = 0`.
    - Toleransi pembulatan (Floating point epsilon) dibatasi pada selisih maksimal `0.01`. Jika selisih absolut > 0.01, maka sistem menandainya sebagai *Unbalanced*.
    """)
