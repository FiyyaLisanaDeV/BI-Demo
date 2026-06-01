import streamlit as st
import graphviz
from src.utils import check_password

st.set_page_config(page_title="Data Lineage Catalog", layout="wide", page_icon="🗺️")

if not check_password():
    st.stop()

st.title("🗺️ Data Lineage & Metadata Catalog")
st.markdown("""
Halaman ini menampilkan peta silsilah aliran data (*Data Provenance* / *Data Lineage*) secara interaktif. 
Grafik ini memvisualisasikan bagaimana setiap tabel mentah (Bronze Layer) diekstraksi, digabungkan, dan ditransformasikan menjadi Data Mart (Gold Layer), hingga akhirnya dikonsumsi oleh masing-masing Dasbor.
""")

st.markdown("---")

def render_lineage():
    # Use dot engine for hierarchical left-to-right layout
    graph = graphviz.Digraph(engine='dot')
    graph.attr(rankdir='LR', size='12,12', nodesep='0.6', ranksep='2.5')
    graph.attr('node', shape='box', style='filled', fontname='Helvetica', fontsize='12', rx='5', ry='5')

    # ==========================================
    # Layer 1: Bronze (Raw Data / Source System)
    # ==========================================
    with graph.subgraph(name='cluster_raw') as c:
        c.attr(label='Bronze Layer (Raw Excel Sources)', style='dashed', color='gray', fontname='Helvetica-Bold')
        c.node_attr.update(color='#FFDDC1', fillcolor='#FFE5CC')
        c.node('raw_emp', '02_employees')
        c.node('raw_cust', '03_customers')
        c.node('raw_sav', '04_accounts_savings')
        c.node('raw_dep', '05_accounts_deposit')
        c.node('raw_loan', '06_loans')
        c.node('raw_txn', '08_transactions')
        c.node('raw_gl', '10_gl_acc & 11_gl_jrn')
        c.node('raw_col', '12_collection_activity')
        c.node('raw_exp', '13_expense_operational')
        c.node('raw_aud', '14_audit_trail')
        c.node('raw_com', '15_customer_complaints')
        c.node('raw_snap', '16_monthly_snapshot')

    # ==========================================
    # Layer 2: Gold (Data Marts)
    # ==========================================
    with graph.subgraph(name='cluster_mart') as c:
        c.attr(label='Gold Layer (Data Mart / Parquet)', style='dashed', color='gold', fontname='Helvetica-Bold')
        c.node_attr.update(color='#D4E157', fillcolor='#E6EE9C')
        c.node('mart_exec', 'mart_executive_summary')
        c.node('mart_dpk', 'mart_dpk\n(Joined with Customer)')
        c.node('mart_loan', 'mart_loans\n(Joined: Cust & Emp)')
        c.node('mart_npl', 'mart_npl')
        c.node('mart_txn', 'mart_transactions')
        c.node('mart_exp', 'mart_expense')
        c.node('mart_gl', 'mart_gl\n(Joined: Acc & Jrn)')
        c.node('mart_kyc', 'mart_customer_kyc')
        c.node('mart_aud', 'mart_audit')
        c.node('mart_com', 'mart_complaints')
        c.node('mart_col', 'mart_collection')
        c.node('mart_kpi', 'mart_kpi_sdm\n(Joined: Emp & Loans)')

    # ==========================================
    # Layer 3: Presentation (Dashboards)
    # ==========================================
    with graph.subgraph(name='cluster_dash') as c:
        c.attr(label='Presentation Layer (Streamlit Pages)', style='dashed', color='blue', fontname='Helvetica-Bold')
        c.node_attr.update(color='#81D4FA', fillcolor='#B3E5FC')
        c.node('d_exec', '01_Executive_Summary')
        c.node('d_dpk', '02_DPK_Dashboard')
        c.node('d_kredit', '03_Kredit_Dashboard')
        c.node('d_npl', '04_NPL_Collection')
        c.node('d_txn', '05_Transactions')
        c.node('d_exp', '06_Expense_Monitoring')
        c.node('d_gl', '07_GL_Accounting')
        c.node('d_kyc', '08_Customer_KYC')
        c.node('d_aud', '09_Audit_Risk')
        c.node('d_com', '10_Complaints')
        c.node('d_kpi', '12_SDM_KPI')

    # ==========================================
    # Edge Mappings (Data Flows)
    # ==========================================
    # Raw -> Mart
    graph.edge('raw_snap', 'mart_exec', label=' Copy')
    
    # DPK Mapping
    graph.edge('raw_sav', 'mart_dpk', label=' Union')
    graph.edge('raw_dep', 'mart_dpk', label=' Union')
    graph.edge('raw_cust', 'mart_dpk', label=' Left Join')
    
    # Loans Mapping
    graph.edge('raw_loan', 'mart_loan', label=' Base')
    graph.edge('raw_cust', 'mart_loan', label=' Left Join')
    graph.edge('raw_emp', 'mart_loan', label=' Left Join')
    
    # NPL & Collection
    graph.edge('raw_loan', 'mart_npl', label=' Filter NPL')
    graph.edge('raw_col', 'mart_col', label=' Copy')
    
    # KPI SDM Mapping
    graph.edge('raw_emp', 'mart_kpi', label=' Base')
    graph.edge('raw_loan', 'mart_kpi', label=' Group By/Sum')
    
    # 1-to-1 Mappings
    graph.edge('raw_txn', 'mart_txn', label=' Cast Types')
    graph.edge('raw_exp', 'mart_exp', label=' Format Date')
    graph.edge('raw_gl', 'mart_gl', label=' Join Keys')
    graph.edge('raw_cust', 'mart_kyc', label=' Copy')
    graph.edge('raw_aud', 'mart_aud', label=' Copy')
    graph.edge('raw_com', 'mart_com', label=' Copy')

    # Mart -> Dashboard
    graph.edge('mart_exec', 'd_exec')
    graph.edge('mart_dpk', 'd_dpk')
    graph.edge('mart_loan', 'd_kredit')
    graph.edge('mart_npl', 'd_npl')
    graph.edge('mart_col', 'd_npl') # NPL dash uses both NPL and Collection
    graph.edge('mart_txn', 'd_txn')
    graph.edge('mart_exp', 'd_exp')
    graph.edge('mart_gl', 'd_gl')
    graph.edge('mart_kyc', 'd_kyc')
    graph.edge('mart_aud', 'd_aud')
    graph.edge('mart_com', 'd_com')
    graph.edge('mart_kpi', 'd_kpi')

    st.graphviz_chart(graph, use_container_width=True)

# Render the interactive graph
render_lineage()

st.markdown("---")
st.markdown("""
**💡 Cara Membaca Data Lineage:**
1. **Bronze Layer (Orange):** Mewakili tabel *raw data* yang diekstrak langsung dari file sistem.
2. **Gold Layer (Hijau Kuning):** Mewakili proses ETL (*Extract, Transform, Load*). Perhatikan garis penghubung (*edges*)! Garis dengan label *Join* atau *Union* menunjukkan adanya penggabungan dua tabel yang berbeda di tingkat *backend*.
3. **Presentation Layer (Biru):** Mewakili halaman akhir dasbor tempat data tersebut dikonsumsi oleh pengguna/analis bisnis. Beberapa dasbor (seperti `04_NPL_Collection`) mengonsumsi lebih dari satu Data Mart secara bersamaan.
""")
