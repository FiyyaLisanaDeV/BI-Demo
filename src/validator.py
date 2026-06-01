import pandas as pd
from typing import Dict, List, Tuple
from .schema import REQUIRED_COLUMNS, ENUM_VALUES, COLUMN_TYPES

class DataValidator:
    def __init__(self, raw_data_path: str):
        self.raw_data_path = raw_data_path
        self.report = []

    def validate_all(self) -> pd.DataFrame:
        print(f"Loading data from {self.raw_data_path}...")
        try:
            self.xls = pd.ExcelFile(self.raw_data_path)
        except Exception as e:
            self.report.append({"table": "ALL", "check_type": "FILE_LOAD", "status": "FAIL", "message": str(e)})
            return pd.DataFrame(self.report)

        for sheet_name in self.xls.sheet_names:
            table_name = sheet_name.split('_', 1)[1] if '_' in sheet_name else sheet_name
            print(f"Validating {table_name}...")
            df = pd.read_excel(self.xls, sheet_name=sheet_name)
            
            self._check_required_columns(table_name, df)
            self._check_forbidden_columns(table_name, df)
            
            if table_name == "gl_journal":
                self._check_gl_balance(df)
            
            if table_name == "loans":
                self._check_loan_validity(df)
                
            if table_name == "accounts_savings":
                self._check_savings_validity(df)

        return pd.DataFrame(self.report)

    def _check_required_columns(self, table_name: str, df: pd.DataFrame):
        req_cols = REQUIRED_COLUMNS.get(table_name, [])
        missing = [c for c in req_cols if c not in df.columns]
        if missing:
            self.report.append({"table": table_name, "check_type": "REQUIRED_COLS", "status": "FAIL", "message": f"Missing columns: {missing}"})
        else:
            self.report.append({"table": table_name, "check_type": "REQUIRED_COLS", "status": "PASS", "message": "All required columns present"})

    def _check_forbidden_columns(self, table_name: str, df: pd.DataFrame):
        forbidden = ["branch_id", "branch_office"]
        found = [c for c in forbidden if c in df.columns]
        if found:
            self.report.append({"table": table_name, "check_type": "FORBIDDEN_COLS", "status": "FAIL", "message": f"Found forbidden columns: {found}"})
        else:
            self.report.append({"table": table_name, "check_type": "FORBIDDEN_COLS", "status": "PASS", "message": "No forbidden columns"})

    def _check_gl_balance(self, df: pd.DataFrame):
        imbalance = df.groupby('journal_id')[['debit_amount', 'credit_amount']].sum()
        imbalance['diff'] = imbalance['debit_amount'] - imbalance['credit_amount']
        errors = imbalance[abs(imbalance['diff']) > 0.01]
        
        if not errors.empty:
            self.report.append({"table": "gl_journal", "check_type": "GL_BALANCE", "status": "FAIL", "message": f"Found {len(errors)} imbalanced journals"})
        else:
            self.report.append({"table": "gl_journal", "check_type": "GL_BALANCE", "status": "PASS", "message": "All journals are balanced"})

    def _check_loan_validity(self, df: pd.DataFrame):
        if 'outstanding_principal' in df.columns:
            neg_out = df[df['outstanding_principal'] < 0]
            if not neg_out.empty:
                self.report.append({"table": "loans", "check_type": "NEGATIVE_OUTSTANDING", "status": "FAIL", "message": f"Found {len(neg_out)} negative outstanding"})
            else:
                self.report.append({"table": "loans", "check_type": "NEGATIVE_OUTSTANDING", "status": "PASS", "message": "No negative outstanding"})
                
        if 'tenor_month' in df.columns:
            invalid_tenor = df[df['tenor_month'] <= 0]
            if not invalid_tenor.empty:
                self.report.append({"table": "loans", "check_type": "INVALID_TENOR", "status": "FAIL", "message": f"Found {len(invalid_tenor)} tenor <= 0"})
            else:
                self.report.append({"table": "loans", "check_type": "INVALID_TENOR", "status": "PASS", "message": "All tenor > 0"})

    def _check_savings_validity(self, df: pd.DataFrame):
        if 'current_balance' in df.columns:
            neg_bal = df[df['current_balance'] < 0]
            if not neg_bal.empty:
                self.report.append({"table": "accounts_savings", "check_type": "NEGATIVE_BALANCE", "status": "FAIL", "message": f"Found {len(neg_bal)} negative balance"})
            else:
                self.report.append({"table": "accounts_savings", "check_type": "NEGATIVE_BALANCE", "status": "PASS", "message": "No negative savings balance"})
