import pandas as pd
import streamlit as st

def render_summary(df: pd.DataFrame, page_context: str):
    """
    Menghasilkan narasi ringkasan secara dinamis berdasarkan data yang sedang difilter.
    """
    if df.empty:
        return
        
    summary_text = ""
    
    try:
        if page_context == "executive":
            latest = df.sort_values('snapshot_date', ascending=False).iloc[0]
            summary_text = f"💡 **Ringkasan Eksekutif:** Pada periode snapshot terbaru ({pd.to_datetime(latest['snapshot_date']).strftime('%B %Y')}), total dana pihak ketiga (DPK) mencapai **Rp {latest['total_savings_balance'] + latest['total_deposit_balance']:,.2f}**, sedangkan total penyaluran kredit (Outstanding) sebesar **Rp {latest['total_loan_outstanding']:,.2f}**. Kualitas kredit (NPL) tercatat di angka **{latest['npl_ratio']*100:.2f}%** dengan profitabilitas berjalan sebelum pajak menyentuh **Rp {latest['profit_loss_before_tax']:,.2f}**. Secara keseluruhan melayani **{latest['total_customers']:,}** nasabah aktif."
            
        elif page_context == "dpk":
            tot_sav = df[df['account_type'] == 'SAVINGS']['balance'].sum() if 'account_type' in df.columns else 0
            tot_dep = df[df['account_type'] == 'DEPOSIT']['balance'].sum() if 'account_type' in df.columns else 0
            tot_acc = len(df)
            top_prod = df.groupby('product_name')['balance'].sum().idxmax() if 'product_name' in df.columns else "N/A"
            summary_text = f"💡 **Ringkasan DPK:** Dari filter yang dipilih, saat ini terdapat **{tot_acc:,} rekening** DPK aktif dengan total dana mencapai **Rp {tot_sav + tot_dep:,.2f}**. Komposisi didominasi oleh produk **{top_prod}**. Porsi tabungan adalah Rp {tot_sav:,.2f} dan porsi deposito adalah Rp {tot_dep:,.2f}."
            
        elif page_context == "kredit":
            tot_loan = df['principal_balance'].sum() if 'principal_balance' in df.columns else 0
            tot_acc = len(df)
            avg_rate = df['interest_rate'].mean() if 'interest_rate' in df.columns else 0
            top_sector = df.groupby('business_sector')['principal_balance'].sum().idxmax() if 'business_sector' in df.columns else "N/A"
            summary_text = f"💡 **Ringkasan Kredit:** Portofolio kredit untuk filter saat ini mencakup **{tot_acc:,} rekening** dengan total baki debet (Outstanding) **Rp {tot_loan:,.2f}**. Rata-rata suku bunga berada di level **{avg_rate*100:.1f}%**. Sektor penyaluran terbesar adalah **{top_sector}**."
            
        elif page_context == "npl":
            tot_loan = df['principal_balance'].sum() if 'principal_balance' in df.columns else 0
            is_npl_df = df[df['is_npl'] == True] if 'is_npl' in df.columns else pd.DataFrame()
            npl_amount = is_npl_df['principal_balance'].sum() if not is_npl_df.empty else 0
            npl_ratio = (npl_amount / tot_loan * 100) if tot_loan > 0 else 0
            summary_text = f"💡 **Ringkasan Kualitas Aktiva:** Dari total baki debet Rp {tot_loan:,.2f}, terdapat **Rp {npl_amount:,.2f}** yang tergolong NPL (Non-Performing Loan). Rasio NPL untuk data yang difilter saat ini adalah **{npl_ratio:.2f}%**. Jumlah rekening bermasalah mencapai **{len(is_npl_df):,}** rekening."
            
        elif page_context == "transactions":
            tot_vol = len(df)
            tot_val = df['amount'].sum() if 'amount' in df.columns else 0
            cash_in = df[(df['transaction_status'] == 'SUCCESS') & (df['debit_credit'] == 'CREDIT')]['amount'].sum() if 'debit_credit' in df.columns else 0
            cash_out = df[(df['transaction_status'] == 'SUCCESS') & (df['debit_credit'] == 'DEBIT')]['amount'].sum() if 'debit_credit' in df.columns else 0
            summary_text = f"💡 **Ringkasan Transaksi:** Terjadi **{tot_vol:,}** mutasi transaksi dengan perputaran dana (Volume) mencapai **Rp {tot_val:,.2f}**. Dari mutasi sukses, tercatat aliran dana masuk (Cash In) sebesar **Rp {cash_in:,.2f}** berbanding aliran dana keluar (Cash Out) sebesar **Rp {cash_out:,.2f}**."

        elif page_context == "expense":
            tot_exp = df['amount'].sum() if 'amount' in df.columns else 0
            top_cat = df.groupby('category')['amount'].sum().idxmax() if 'category' in df.columns else "N/A"
            summary_text = f"💡 **Ringkasan Biaya Operasional:** Total biaya operasional yang tercatat pada rentang filter ini mencapai **Rp {tot_exp:,.2f}**. Pengeluaran paling besar terserap pada kategori **{top_cat}**."

        elif page_context == "gl":
            tot_debit = df['debit_amount'].sum() if 'debit_amount' in df.columns else 0
            tot_credit = df['credit_amount'].sum() if 'credit_amount' in df.columns else 0
            status = "SEIMBANG (Balanced)" if abs(tot_debit - tot_credit) < 0.01 else "TIDAK SEIMBANG (Unbalanced)"
            summary_text = f"💡 **Ringkasan Buku Besar (GL):** Transaksi jurnal yang difilter mencatat total mutasi Debit **Rp {tot_debit:,.2f}** dan Kredit **Rp {tot_credit:,.2f}**. Status keseimbangan jurnal saat ini: **{status}**."

        elif page_context == "kyc":
            tot_cust = len(df)
            high_risk = len(df[df.get('risk_profile', df.get('risk_level', pd.Series())) == 'HIGH'])
            summary_text = f"💡 **Ringkasan KYC Nasabah:** Terdapat **{tot_cust:,} profil nasabah** dalam filter aktif. Dari jumlah tersebut, sebanyak **{high_risk:,} nasabah** diklasifikasikan memiliki profil risiko tinggi (High Risk) yang memerlukan pemantauan ketat CDD/EDD."
            
        elif page_context == "audit":
            tot_logs = len(df)
            high_sev = len(df[df['severity'] == 'HIGH']) if 'severity' in df.columns else 0
            summary_text = f"💡 **Ringkasan Audit Trail:** Sistem merekam **{tot_logs:,} aktivitas** di rentang filter ini. Terdapat **{high_sev:,} peringatan aktivitas** dengan level tingkat keparahan tinggi (High Severity) yang mencurigakan."

        elif page_context == "complaints":
            tot_comp = len(df)
            unresolved = len(df[df['status'] != 'RESOLVED']) if 'status' in df.columns else 0
            summary_text = f"💡 **Ringkasan Layanan Pengaduan:** Terdapat **{tot_comp:,} keluhan** nasabah. Saat ini, masih ada **{unresolved:,} tiket pengaduan** yang berstatus belum terselesaikan atau sedang dalam proses investigasi."
            
    except Exception as e:
        summary_text = f"💡 **Catatan Sistem:** Sedang menghitung ulang ringkasan dinamis... (Data baru saja berubah)"
        
    if summary_text:
        st.info(summary_text)
