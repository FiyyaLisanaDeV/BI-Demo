import pandas as pd
from typing import Dict

class DataTransformer:
    def __init__(self, xls_path: str):
        self.xls = pd.ExcelFile(xls_path)
        # Load tables
        self.df_units = self._load_sheet('01_operation_units')
        self.df_employees = self._load_sheet('02_employees')
        self.df_customers = self._load_sheet('03_customers')
        self.df_savings = self._load_sheet('04_accounts_savings')
        self.df_deposits = self._load_sheet('05_accounts_deposit')
        self.df_loans = self._load_sheet('06_loans')
        self.df_transactions = self._load_sheet('08_transactions')
        self.df_gl_acc = self._load_sheet('10_gl_accounts')
        self.df_gl_jrn = self._load_sheet('11_gl_journal')
        self.df_collection = self._load_sheet('12_collection_activity')
        self.df_expense = self._load_sheet('13_expense_operational')
        self.df_audit = self._load_sheet('14_audit_trail')
        self.df_complaints = self._load_sheet('15_customer_complaints')
        self.df_snapshot = self._load_sheet('16_monthly_snapshot')

    def _load_sheet(self, sheet_name):
        try:
            return pd.read_excel(self.xls, sheet_name=sheet_name)
        except:
            return pd.DataFrame()

    def build_mart_executive_summary(self) -> pd.DataFrame:
        if self.df_snapshot.empty: return pd.DataFrame()
        return self.df_snapshot

    def build_mart_dpk(self) -> pd.DataFrame:
        # Savings
        if self.df_savings.empty and self.df_deposits.empty: return pd.DataFrame()
        sav = self.df_savings.copy()
        if not sav.empty:
            sav['account_type'] = 'SAVINGS'
            sav = sav.rename(columns={'savings_account_id': 'account_id', 'current_balance': 'balance'})
        
        # Deposits
        dep = self.df_deposits.copy()
        if not dep.empty:
            dep['account_type'] = 'DEPOSIT'
            dep = dep.rename(columns={'deposit_account_id': 'account_id', 'principal_amount': 'balance'})
            
        combined = pd.concat([sav, dep], ignore_index=True)
        if not combined.empty and not self.df_customers.empty:
            combined = combined.merge(self.df_customers[['customer_id', 'full_name', 'customer_type']], on='customer_id', how='left')
        return combined

    def build_mart_loans(self) -> pd.DataFrame:
        if self.df_loans.empty: return pd.DataFrame()
        df = self.df_loans.copy()
        if not self.df_customers.empty:
            df = df.merge(self.df_customers[['customer_id', 'full_name', 'customer_type', 'business_sector']], on='customer_id', how='left')
        if not self.df_employees.empty:
            df = df.merge(self.df_employees[['employee_id', 'full_name']].rename(columns={'employee_id': 'loan_officer_id', 'full_name': 'ao_name'}), on='loan_officer_id', how='left')
        return df

    def build_mart_npl(self) -> pd.DataFrame:
        if self.df_loans.empty: return pd.DataFrame()
        npl_status = ['KURANG_LANCAR', 'DIRAGUKAN', 'MACET']
        df = self.df_loans.copy()
        df['is_npl'] = df['collectability_status'].isin(npl_status)
        return df

    def build_mart_transactions(self) -> pd.DataFrame:
        if self.df_transactions.empty: return pd.DataFrame()
        df = self.df_transactions.copy()
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['date_only'] = df['transaction_date'].dt.date
        return df

    def build_mart_expense(self) -> pd.DataFrame:
        if self.df_expense.empty: return pd.DataFrame()
        df = self.df_expense.copy()
        df['expense_date'] = pd.to_datetime(df['expense_date'])
        df['month_year'] = df['expense_date'].dt.to_period('M')
        return df

    def build_mart_gl(self) -> pd.DataFrame:
        if self.df_gl_jrn.empty or self.df_gl_acc.empty: return pd.DataFrame()
        df = self.df_gl_jrn.merge(self.df_gl_acc, on='gl_account_id', how='left')
        return df

    def build_mart_customer_kyc(self) -> pd.DataFrame:
        if self.df_customers.empty: return pd.DataFrame()
        return self.df_customers.copy()
        
    def build_mart_audit(self) -> pd.DataFrame:
        if self.df_audit.empty: return pd.DataFrame()
        return self.df_audit.copy()

    def build_mart_complaints(self) -> pd.DataFrame:
        if self.df_complaints.empty: return pd.DataFrame()
        return self.df_complaints.copy()

    def build_mart_collection(self) -> pd.DataFrame:
        if self.df_collection.empty: return pd.DataFrame()
        return self.df_collection.copy()

    def build_mart_kpi_sdm(self) -> pd.DataFrame:
        if self.df_employees.empty: return pd.DataFrame()
        df = self.df_employees.copy()
        
        # Calculate Loan Portfolio size per AO
        if not self.df_loans.empty:
            loans = self.df_loans.groupby('loan_officer_id')['outstanding_principal'].sum().reset_index()
            loans = loans.rename(columns={'loan_officer_id': 'employee_id', 'outstanding_principal': 'total_loan_portfolio'})
            df = df.merge(loans, on='employee_id', how='left')
            df['total_loan_portfolio'] = df['total_loan_portfolio'].fillna(0)
            
        # Target simulation
        df['kpi_target'] = df['position'].apply(lambda x: 500000000 if 'Manager' in str(x) else 150000000)
        if 'total_loan_portfolio' in df.columns:
            df['achievement_percentage'] = (df['total_loan_portfolio'] / df['kpi_target'] * 100).fillna(0)
        else:
            df['total_loan_portfolio'] = 0
            df['achievement_percentage'] = 0
            
        return df

    def build_all_marts(self) -> Dict[str, pd.DataFrame]:
        return {
            "mart_executive_summary": self.build_mart_executive_summary(),
            "mart_dpk": self.build_mart_dpk(),
            "mart_loans": self.build_mart_loans(),
            "mart_npl": self.build_mart_npl(),
            "mart_transactions": self.build_mart_transactions(),
            "mart_expense": self.build_mart_expense(),
            "mart_gl": self.build_mart_gl(),
            "mart_customer_kyc": self.build_mart_customer_kyc(),
            "mart_audit": self.build_mart_audit(),
            "mart_complaints": self.build_mart_complaints(),
            "mart_collection": self.build_mart_collection(),
            "mart_kpi_sdm": self.build_mart_kpi_sdm()
        }
