import pandas as pd

def calc_total_customers(df: pd.DataFrame) -> int:
    """Returns total number of customers"""
    return len(df) if not df.empty else 0

def calc_total_dpk(df_dpk: pd.DataFrame) -> float:
    """Returns total balance of savings + deposits"""
    return df_dpk['balance'].sum() if not df_dpk.empty else 0.0

def calc_total_loan_outstanding(df_loans: pd.DataFrame) -> float:
    """Returns total outstanding principal"""
    return df_loans['outstanding_principal'].sum() if not df_loans.empty else 0.0

def calc_npl_ratio(df_npl: pd.DataFrame) -> float:
    """Returns NPL Ratio (NPL outstanding / Total outstanding)"""
    if df_npl.empty: return 0.0
    total_out = df_npl['outstanding_principal'].sum()
    if total_out == 0: return 0.0
    npl_out = df_npl[df_npl['is_npl']]['outstanding_principal'].sum()
    return npl_out / total_out

def calc_gl_balance_diff(df_gl: pd.DataFrame) -> float:
    """Returns absolute difference between total debit and total credit"""
    if df_gl.empty: return 0.0
    debit = df_gl['debit_amount'].sum()
    credit = df_gl['credit_amount'].sum()
    return abs(debit - credit)

def calc_cash_in(df_trx: pd.DataFrame) -> float:
    """Returns total cash in from transactions"""
    if df_trx.empty: return 0.0
    return df_trx[df_trx['transaction_status'] == 'SUCCESS']['amount'].sum()

def calc_expense(df_exp: pd.DataFrame) -> float:
    """Returns total operational expense"""
    return df_exp['amount'].sum() if not df_exp.empty else 0.0
