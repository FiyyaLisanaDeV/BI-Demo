REQUIRED_COLUMNS = {
    "operation_units": ["unit_id", "unit_name", "department", "unit_type", "manager_employee_id", "is_active"],
    "employees": ["employee_id", "full_name", "unit_id", "department", "position", "join_date", "employment_status", "supervisor_id", "is_active"],
    "customers": ["customer_id", "customer_type", "full_name", "gender", "birth_date", "age", "id_type", "id_number_dummy", "phone_dummy", "address_city", "address_district", "address_area", "occupation", "business_sector", "monthly_income", "risk_profile", "kyc_status", "customer_since", "is_active"],
    "accounts_savings": ["savings_account_id", "customer_id", "unit_id", "product_name", "open_date", "current_balance", "average_balance_30d", "interest_rate", "account_status", "last_transaction_date", "dormant_flag"],
    "accounts_deposit": ["deposit_account_id", "customer_id", "unit_id", "product_name", "placement_date", "maturity_date", "tenor_month", "principal_amount", "interest_rate", "interest_payment_type", "rollover_type", "deposit_status"],
    "loans": ["loan_id", "customer_id", "unit_id", "loan_product", "loan_purpose", "economic_sector", "approval_date", "disbursement_date", "maturity_date", "principal_amount", "outstanding_principal", "interest_rate", "tenor_month", "installment_amount", "payment_frequency", "collectability_status", "days_past_due", "loan_status", "loan_officer_id", "approval_status", "restructure_flag"],
    "loan_installments": ["installment_id", "loan_id", "due_date", "payment_date", "principal_due", "interest_due", "penalty_due", "total_due", "principal_paid", "interest_paid", "penalty_paid", "total_paid", "payment_status", "days_late", "remaining_principal_after_payment"],
    "transactions": ["transaction_id", "transaction_date", "unit_id", "customer_id", "account_type", "account_id", "transaction_type", "channel", "debit_credit", "amount", "fee_amount", "transaction_status", "teller_id", "description", "reference_no"],
    "collateral": ["collateral_id", "loan_id", "customer_id", "collateral_type", "collateral_description", "estimated_value", "appraised_value", "binding_type", "ownership_status", "document_status", "insurance_status", "last_appraisal_date"],
    "gl_accounts": ["gl_account_id", "gl_code", "gl_name", "gl_category", "normal_balance", "is_active"],
    "gl_journal": ["journal_id", "journal_date", "unit_id", "source_module", "source_reference_id", "gl_account_id", "debit_amount", "credit_amount", "description", "posted_by", "posted_at", "posting_status"],
    "collection_activity": ["collection_id", "loan_id", "customer_id", "collector_id", "activity_date", "activity_type", "contact_result", "promise_to_pay_date", "promise_to_pay_amount", "next_follow_up_date", "collection_notes", "risk_escalation"],
    "expense_operational": ["expense_id", "expense_date", "unit_id", "department", "expense_category", "vendor_name", "amount", "payment_method", "approval_status", "approved_by", "description"],
    "audit_trail": ["audit_id", "event_time", "user_id", "employee_id", "unit_id", "module_name", "action_type", "record_id", "old_value_dummy", "new_value_dummy", "ip_address_dummy", "device_type", "risk_flag"],
    "customer_complaints": ["complaint_id", "complaint_date", "customer_id", "employee_id", "unit_id", "complaint_channel", "complaint_category", "priority", "status", "description", "resolution_date", "resolution_notes", "resolution_days"],
    "monthly_snapshot": ["snapshot_id", "snapshot_date", "total_customers", "total_savings_balance", "total_deposit_balance", "total_loan_outstanding", "npl_ratio", "total_transactions", "cash_in", "cash_out", "total_operational_expense", "profit_loss_before_tax"]
}

COLUMN_TYPES = {
    # Tipe data ini hanya sebagai pedoman validasi dasar
    "int": ["age", "tenor_month", "days_past_due", "days_late", "resolution_days"],
    "float": ["monthly_income", "current_balance", "average_balance_30d", "interest_rate", "principal_amount", "outstanding_principal", "installment_amount", "principal_due", "interest_due", "penalty_due", "total_due", "principal_paid", "interest_paid", "penalty_paid", "total_paid", "remaining_principal_after_payment", "amount", "fee_amount", "estimated_value", "appraised_value", "debit_amount", "credit_amount", "promise_to_pay_amount", "total_savings_balance", "total_deposit_balance", "total_loan_outstanding", "npl_ratio", "cash_in", "cash_out", "total_operational_expense", "profit_loss_before_tax"],
    "date": ["birth_date", "customer_since", "open_date", "last_transaction_date", "placement_date", "maturity_date", "approval_date", "disbursement_date", "due_date", "payment_date", "transaction_date", "last_appraisal_date", "journal_date", "activity_date", "promise_to_pay_date", "next_follow_up_date", "expense_date", "event_time", "complaint_date", "resolution_date", "snapshot_date"],
    "bool": ["is_active", "dormant_flag", "restructure_flag"]
}

ENUM_VALUES = {
    "customer_type": ["INDIVIDU", "UMKM", "BADAN_USAHA"],
    "gender": ["L", "P"],
    "kyc_status": ["COMPLETE", "INCOMPLETE", "NEED_REVIEW"],
    "account_status": ["ACTIVE", "DORMANT", "CLOSED", "BLOCKED"],
    "deposit_status": ["ACTIVE", "MATURED", "CLOSED"],
    "collectability_status": ["LANCAR", "DPK", "KURANG_LANCAR", "DIRAGUKAN", "MACET"],
    "loan_status": ["ACTIVE", "PAID_OFF", "WRITTEN_OFF", "RESTRUCTURED"],
    "transaction_status": ["SUCCESS", "REVERSED", "PENDING", "FAILED"],
    "posting_status": ["POSTED", "DRAFT", "REVERSED"]
}

def get_required_columns(table_name):
    return REQUIRED_COLUMNS.get(table_name, [])

def list_tables():
    return list(REQUIRED_COLUMNS.keys())
