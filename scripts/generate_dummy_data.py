import os
import sys
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Tambahkan root path ke sys.path agar bisa import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.schema import REQUIRED_COLUMNS, ENUM_VALUES

# Inisialisasi Faker dengan seed agar konsisten
fake = Faker('id_ID')
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# ==========================================
# Parameter Jumlah Data (Sesuai Permintaan)
# ==========================================
NUM_UNITS = 10
NUM_EMPLOYEES = 100
NUM_CUSTOMERS = 3000
NUM_SAVINGS = 3500
NUM_DEPOSITS = 700
NUM_LOANS = 1500
NUM_INSTALLMENTS = 6000
NUM_TRANSACTIONS = 10000
NUM_COLLATERALS = 1300
NUM_GL_ACCOUNTS = 50
NUM_GL_JOURNALS = 6000
NUM_COLLECTION_ACTIVITY = 2000
NUM_EXPENSES = 1000
NUM_AUDIT_TRAIL = 5000
NUM_COMPLAINTS = 500
NUM_SNAPSHOTS = 24

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(OUTPUT_DIR, exist_ok=True)
EXCEL_OUTPUT = os.path.join(OUTPUT_DIR, 'bpr_simulasi_dummy_dataset.xlsx')

def generate_operation_units():
    data = []
    departments = ["OPERASIONAL", "KREDIT", "DANA", "COLLECTION", "KEUANGAN", "IT", "COMPLIANCE", "AUDIT_INTERNAL", "MANAGEMENT", "TELLER_CS"]
    unit_types = ["FRONT_OFFICE", "BACK_OFFICE", "CONTROL", "MANAGEMENT"]
    
    for i in range(1, NUM_UNITS + 1):
        dept = departments[i % len(departments)]
        data.append({
            "unit_id": f"UNIT_{i:03d}",
            "unit_name": f"Unit {dept.capitalize()}",
            "department": dept,
            "unit_type": random.choice(unit_types),
            "manager_employee_id": f"EMP{random.randint(1, NUM_EMPLOYEES):06d}",
            "is_active": True
        })
    return pd.DataFrame(data)

def generate_employees(units_df):
    data = []
    positions = ["TELLER", "CUSTOMER_SERVICE", "ACCOUNT_OFFICER", "KOLEKTOR", "AKUNTANSI", "COMPLIANCE_OFFICER", "AUDITOR_INTERNAL", "MANAGER"]
    unit_ids = units_df['unit_id'].tolist()
    
    for i in range(1, NUM_EMPLOYEES + 1):
        data.append({
            "employee_id": f"EMP{i:06d}",
            "full_name": fake.name(),
            "unit_id": random.choice(unit_ids),
            "department": random.choice(["OPERASIONAL", "KREDIT", "DANA", "COLLECTION", "KEUANGAN", "IT", "COMPLIANCE", "AUDIT_INTERNAL"]),
            "position": random.choice(positions),
            "join_date": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d"),
            "employment_status": random.choice(["PERMANENT", "CONTRACT"]),
            "supervisor_id": f"EMP{random.randint(1, NUM_EMPLOYEES):06d}",
            "is_active": random.choice([True, True, True, False])
        })
    return pd.DataFrame(data)

def generate_customers():
    data = []
    cities = ["KENDARI", "KENDARI", "KENDARI", "KONAWE", "KOLAKA"]
    districts = ["MANDONGA", "BARUGA", "WUA_WUA", "KADIA", "POASIA", "ABELI", "KAMBU", "PUUWATU"]
    areas = ["PASAR", "PERUMAHAN", "PESISIR", "KAMPUS", "PERKANTORAN", "USAHA_MIKRO"]
    occupations = ["PNS", "KARYAWAN", "PEDAGANG", "NELAYAN", "PETANI", "WIRASWASTA", "HONORER", "IRT"]
    sectors = ["PERDAGANGAN", "PERTANIAN", "JASA", "PERIKANAN", "KONSTRUKSI", "KONSUMTIF"]
    
    for i in range(1, NUM_CUSTOMERS + 1):
        cust_type = random.choice(ENUM_VALUES["customer_type"])
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)
        age = (datetime.now().date() - birth_date).days // 365
        
        data.append({
            "customer_id": f"CUST{i:06d}",
            "customer_type": cust_type,
            "full_name": fake.company() if cust_type != "INDIVIDU" else fake.name(),
            "gender": random.choice(ENUM_VALUES["gender"]) if cust_type == "INDIVIDU" else None,
            "birth_date": birth_date.strftime("%Y-%m-%d") if cust_type == "INDIVIDU" else None,
            "age": age if cust_type == "INDIVIDU" else None,
            "id_type": "KTP" if cust_type == "INDIVIDU" else "NPWP",
            "id_number_dummy": str(fake.random_number(digits=16, fix_len=True)),
            "phone_dummy": fake.phone_number(),
            "address_city": random.choice(cities),
            "address_district": random.choice(districts),
            "address_area": random.choice(areas),
            "occupation": random.choice(occupations) if cust_type == "INDIVIDU" else "PERUSAHAAN",
            "business_sector": random.choice(sectors),
            "monthly_income": float(random.randint(3000000, 50000000)),
            "risk_profile": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "kyc_status": random.choice(ENUM_VALUES["kyc_status"]),
            "customer_since": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d"),
            "is_active": random.choice([True, True, True, False])
        })
    return pd.DataFrame(data)

def generate_accounts_savings(customers_df, units_df):
    data = []
    products = ["TABUNGAN_BAHTERAMAS", "TABUNGAN_PELAJAR", "TABUNGAN_UMKM", "TABUNGAN_REGULER"]
    unit_ids = units_df['unit_id'].tolist()
    
    for i in range(1, NUM_SAVINGS + 1):
        data.append({
            "savings_account_id": f"SAV{i:06d}",
            "customer_id": random.choice(customers_df['customer_id'].tolist()),
            "unit_id": random.choice(unit_ids),
            "product_name": random.choice(products),
            "open_date": fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d"),
            "current_balance": float(random.randint(10000, 50000000)),
            "average_balance_30d": float(random.randint(10000, 45000000)),
            "interest_rate": round(random.uniform(0.01, 0.05), 4),
            "account_status": random.choice(ENUM_VALUES["account_status"]),
            "last_transaction_date": fake.date_between(start_date="-1m", end_date="today").strftime("%Y-%m-%d"),
            "dormant_flag": random.choice([True, False, False, False])
        })
    return pd.DataFrame(data)

def generate_accounts_deposit(customers_df, units_df):
    data = []
    products = ["DEPOSITO_1_BULAN", "DEPOSITO_3_BULAN", "DEPOSITO_6_BULAN", "DEPOSITO_12_BULAN"]
    unit_ids = units_df['unit_id'].tolist()
    
    for i in range(1, NUM_DEPOSITS + 1):
        placement = fake.date_between(start_date="-2y", end_date="today")
        tenor = random.choice([1, 3, 6, 12])
        maturity = placement + timedelta(days=30*tenor)
        
        data.append({
            "deposit_account_id": f"DEP{i:06d}",
            "customer_id": random.choice(customers_df['customer_id'].tolist()),
            "unit_id": random.choice(unit_ids),
            "product_name": random.choice(products),
            "placement_date": placement.strftime("%Y-%m-%d"),
            "maturity_date": maturity.strftime("%Y-%m-%d"),
            "tenor_month": tenor,
            "principal_amount": float(random.randint(5000000, 500000000)),
            "interest_rate": round(random.uniform(0.04, 0.08), 4),
            "interest_payment_type": random.choice(["MONTHLY", "MATURITY"]),
            "rollover_type": random.choice(["NON_ARO", "ARO_PRINCIPAL", "ARO_PRINCIPAL_INTEREST"]),
            "deposit_status": random.choice(ENUM_VALUES["deposit_status"])
        })
    return pd.DataFrame(data)

def generate_loans(customers_df, units_df, employees_df):
    data = []
    products = ["KREDIT_MODAL_KERJA", "KREDIT_INVESTASI", "KREDIT_KONSUMTIF", "KREDIT_PEGAWAI", "KREDIT_UMKM"]
    purposes = ["MODAL_USAHA", "RENOVASI", "KENDARAAN", "PENDIDIKAN", "KONSUMTIF", "INVESTASI_ALAT"]
    sectors = ["PERDAGANGAN", "PERTANIAN", "PERIKANAN", "JASA", "KONSTRUKSI", "KONSUMTIF"]
    
    aos = employees_df[employees_df['position'] == 'ACCOUNT_OFFICER']['employee_id'].tolist()
    if not aos: aos = employees_df['employee_id'].tolist()
    
    for i in range(1, NUM_LOANS + 1):
        approval = fake.date_between(start_date="-3y", end_date="today")
        tenor = random.choice([12, 24, 36, 48, 60])
        principal = float(random.randint(10000000, 500000000))
        outstanding = float(random.uniform(0, principal))
        
        data.append({
            "loan_id": f"LOAN{i:06d}",
            "customer_id": random.choice(customers_df['customer_id'].tolist()),
            "unit_id": random.choice(units_df['unit_id'].tolist()),
            "loan_product": random.choice(products),
            "loan_purpose": random.choice(purposes),
            "economic_sector": random.choice(sectors),
            "approval_date": approval.strftime("%Y-%m-%d"),
            "disbursement_date": (approval + timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
            "maturity_date": (approval + timedelta(days=30*tenor)).strftime("%Y-%m-%d"),
            "principal_amount": principal,
            "outstanding_principal": outstanding,
            "interest_rate": round(random.uniform(0.12, 0.24), 4),
            "tenor_month": tenor,
            "installment_amount": float((principal / tenor) * 1.2),
            "payment_frequency": "MONTHLY",
            "collectability_status": random.choice(ENUM_VALUES["collectability_status"]),
            "days_past_due": random.randint(0, 150) if random.random() > 0.8 else 0,
            "loan_status": random.choice(ENUM_VALUES["loan_status"]),
            "loan_officer_id": random.choice(aos),
            "approval_status": "APPROVED",
            "restructure_flag": random.choice([True, False, False, False])
        })
    return pd.DataFrame(data)

def generate_loan_installments(loans_df):
    data = []
    loan_ids = loans_df['loan_id'].tolist()
    
    for i in range(1, NUM_INSTALLMENTS + 1):
        due = fake.date_between(start_date="-1y", end_date="+1y")
        principal_due = float(random.randint(500000, 5000000))
        interest_due = float(random.randint(100000, 1000000))
        
        data.append({
            "installment_id": f"INST{i:08d}",
            "loan_id": random.choice(loan_ids),
            "due_date": due.strftime("%Y-%m-%d"),
            "payment_date": (due + timedelta(days=random.randint(-5, 30))).strftime("%Y-%m-%d") if random.random() > 0.1 else None,
            "principal_due": principal_due,
            "interest_due": interest_due,
            "penalty_due": 0.0,
            "total_due": principal_due + interest_due,
            "principal_paid": principal_due if random.random() > 0.2 else 0.0,
            "interest_paid": interest_due if random.random() > 0.2 else 0.0,
            "penalty_paid": 0.0,
            "total_paid": principal_due + interest_due,
            "payment_status": random.choice(["PAID", "PARTIAL", "UNPAID", "LATE"]),
            "days_late": random.randint(0, 60),
            "remaining_principal_after_payment": float(random.randint(0, 100000000))
        })
    return pd.DataFrame(data)

def generate_transactions(savings_df, deposits_df, loans_df, units_df, employees_df):
    data = []
    accounts = []
    for id in savings_df['savings_account_id']: accounts.append(("SAVINGS", id))
    for id in deposits_df['deposit_account_id']: accounts.append(("DEPOSIT", id))
    for id in loans_df['loan_id']: accounts.append(("LOAN", id))
    
    types = ["SETORAN_TABUNGAN", "TARIK_TUNAI", "PENCAIRAN_KREDIT", "BAYAR_ANGSURAN", "PENEMPATAN_DEPOSITO", "BIAYA_ADMIN", "KOREKSI"]
    channels = ["TELLER", "BACKOFFICE", "KOLEKTOR", "TRANSFER_BANK", "MOBILE_COLLECTOR"]
    
    for i in range(1, NUM_TRANSACTIONS + 1):
        acc_type, acc_id = random.choice(accounts)
        amount = float(random.randint(50000, 10000000))
        
        data.append({
            "transaction_id": f"TRX{i:08d}",
            "transaction_date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d %H:%M:%S"),
            "unit_id": random.choice(units_df['unit_id'].tolist()),
            "customer_id": f"CUST{random.randint(1, NUM_CUSTOMERS):06d}",
            "account_type": acc_type,
            "account_id": acc_id,
            "transaction_type": random.choice(types),
            "channel": random.choice(channels),
            "debit_credit": random.choice(["DEBIT", "CREDIT"]),
            "amount": amount,
            "fee_amount": float(random.choice([0, 2500, 5000, 10000])),
            "transaction_status": random.choice(ENUM_VALUES["transaction_status"]),
            "teller_id": random.choice(employees_df['employee_id'].tolist()),
            "description": fake.sentence(nb_words=3),
            "reference_no": fake.uuid4()[:8]
        })
    return pd.DataFrame(data)

def generate_collaterals(loans_df):
    data = []
    types = ["BPKB_MOTOR", "BPKB_MOBIL", "SERTIFIKAT_TANAH", "SK_PEGAWAI", "INVENTORY", "DEPOSITO"]
    bindings = ["FIDUSIA", "HAK_TANGGUNGAN", "GADAI", "KUASA_MENJUAL", "NON_BINDING"]
    
    for i in range(1, NUM_COLLATERALS + 1):
        est_value = float(random.randint(10000000, 500000000))
        data.append({
            "collateral_id": f"COL{i:06d}",
            "loan_id": random.choice(loans_df['loan_id'].tolist()),
            "customer_id": f"CUST{random.randint(1, NUM_CUSTOMERS):06d}",
            "collateral_type": random.choice(types),
            "collateral_description": fake.sentence(nb_words=4),
            "estimated_value": est_value,
            "appraised_value": est_value * random.uniform(0.8, 1.2),
            "binding_type": random.choice(bindings),
            "ownership_status": random.choice(["MILIK_SENDIRI", "MILIK_KELUARGA", "MILIK_USAHA"]),
            "document_status": random.choice(["COMPLETE", "INCOMPLETE", "EXPIRED", "NEED_REVIEW"]),
            "insurance_status": random.choice(["INSURED", "NOT_INSURED", "EXPIRED"]),
            "last_appraisal_date": fake.date_between(start_date="-2y", end_date="today").strftime("%Y-%m-%d")
        })
    return pd.DataFrame(data)

def generate_gl_accounts():
    data = []
    categories = ["ASET", "LIABILITAS", "EKUITAS", "PENDAPATAN", "BEBAN"]
    
    # Generate some standard accounts
    standard_accounts = [
        ("1001", "Kas Teller", "ASET", "DEBIT"),
        ("1002", "Kas Besar", "ASET", "DEBIT"),
        ("1201", "Kredit Yang Diberikan", "ASET", "DEBIT"),
        ("2101", "Tabungan Nasabah", "LIABILITAS", "CREDIT"),
        ("2201", "Deposito Nasabah", "LIABILITAS", "CREDIT"),
        ("3101", "Modal Disetor", "EKUITAS", "CREDIT"),
        ("4101", "Pendapatan Bunga Kredit", "PENDAPATAN", "CREDIT"),
        ("5101", "Beban Bunga Tabungan", "BEBAN", "DEBIT"),
        ("5201", "Beban Operasional", "BEBAN", "DEBIT"),
    ]
    
    for idx, (code, name, cat, bal) in enumerate(standard_accounts, 1):
        data.append({
            "gl_account_id": f"GL{idx:04d}",
            "gl_code": code,
            "gl_name": name,
            "gl_category": cat,
            "normal_balance": bal,
            "is_active": True
        })
        
    # Generate remaining dummy accounts
    for i in range(len(standard_accounts) + 1, NUM_GL_ACCOUNTS + 1):
        cat = random.choice(categories)
        bal = "DEBIT" if cat in ["ASET", "BEBAN"] else "CREDIT"
        data.append({
            "gl_account_id": f"GL{i:04d}",
            "gl_code": str(random.randint(1000, 9999)),
            "gl_name": f"Akun {fake.word().capitalize()}",
            "gl_category": cat,
            "normal_balance": bal,
            "is_active": True
        })
    return pd.DataFrame(data)

def generate_gl_journals(gl_accounts_df, units_df):
    data = []
    modules = ["SAVINGS", "DEPOSIT", "LOAN", "TELLER", "EXPENSE", "ADJUSTMENT"]
    
    # We create journal entries in pairs (Debit and Credit) so it balances
    entry_id = 1
    for i in range(1, NUM_GL_JOURNALS // 2 + 1):
        journal_id = f"JRN{i:08d}"
        journal_date = fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
        unit_id = random.choice(units_df['unit_id'].tolist())
        amount = float(random.randint(10000, 50000000))
        
        acc1 = random.choice(gl_accounts_df['gl_account_id'].tolist())
        acc2 = random.choice(gl_accounts_df['gl_account_id'].tolist())
        while acc1 == acc2: acc2 = random.choice(gl_accounts_df['gl_account_id'].tolist())
        
        # Debit entry
        data.append({
            "journal_id": journal_id,
            "journal_date": journal_date,
            "unit_id": unit_id,
            "source_module": random.choice(modules),
            "source_reference_id": f"REF{random.randint(1, 1000):04d}",
            "gl_account_id": acc1,
            "debit_amount": amount,
            "credit_amount": 0.0,
            "description": fake.sentence(nb_words=3),
            "posted_by": f"EMP{random.randint(1, NUM_EMPLOYEES):06d}",
            "posted_at": f"{journal_date} 12:00:00",
            "posting_status": random.choice(ENUM_VALUES["posting_status"])
        })
        
        # Credit entry
        data.append({
            "journal_id": journal_id,
            "journal_date": journal_date,
            "unit_id": unit_id,
            "source_module": random.choice(modules),
            "source_reference_id": f"REF{random.randint(1, 1000):04d}",
            "gl_account_id": acc2,
            "debit_amount": 0.0,
            "credit_amount": amount,
            "description": fake.sentence(nb_words=3),
            "posted_by": f"EMP{random.randint(1, NUM_EMPLOYEES):06d}",
            "posted_at": f"{journal_date} 12:00:00",
            "posting_status": random.choice(ENUM_VALUES["posting_status"])
        })
        
    return pd.DataFrame(data)

def generate_collection_activity(loans_df, employees_df):
    data = []
    types = ["CALL", "VISIT", "WHATSAPP", "SURAT_PERINGATAN", "NEGOSIASI", "PENAGIHAN_LAPANGAN"]
    results = ["CONNECTED", "NO_RESPONSE", "PROMISE_TO_PAY", "REFUSED", "WRONG_NUMBER", "CUSTOMER_NOT_FOUND"]
    
    for i in range(1, NUM_COLLECTION_ACTIVITY + 1):
        activity_date = fake.date_between(start_date="-6m", end_date="today")
        data.append({
            "collection_id": f"CA{i:06d}",
            "loan_id": random.choice(loans_df['loan_id'].tolist()),
            "customer_id": f"CUST{random.randint(1, NUM_CUSTOMERS):06d}",
            "collector_id": random.choice(employees_df['employee_id'].tolist()),
            "activity_date": activity_date.strftime("%Y-%m-%d"),
            "activity_type": random.choice(types),
            "contact_result": random.choice(results),
            "promise_to_pay_date": (activity_date + timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d") if random.random() > 0.5 else None,
            "promise_to_pay_amount": float(random.randint(500000, 5000000)) if random.random() > 0.5 else 0.0,
            "next_follow_up_date": (activity_date + timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
            "collection_notes": fake.sentence(),
            "risk_escalation": random.choice(["NORMAL", "WATCHLIST", "LEGAL_REVIEW", "RESTRUCTURE_REVIEW"])
        })
    return pd.DataFrame(data)

def generate_expense_operational(units_df):
    data = []
    categories = ["ATK", "LISTRIK", "INTERNET", "SEWA", "TRANSPORT", "MAINTENANCE", "KONSUMSI", "OPERASIONAL_KANTOR", "BIAYA_PENAGIHAN"]
    
    for i in range(1, NUM_EXPENSES + 1):
        data.append({
            "expense_id": f"EXP{i:06d}",
            "expense_date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d"),
            "unit_id": random.choice(units_df['unit_id'].tolist()),
            "department": random.choice(["OPERASIONAL", "KREDIT", "COLLECTION", "KEUANGAN", "IT", "COMPLIANCE", "AUDIT_INTERNAL"]),
            "expense_category": random.choice(categories),
            "vendor_name": fake.company(),
            "amount": float(random.randint(100000, 15000000)),
            "payment_method": random.choice(["CASH", "TRANSFER", "PETTY_CASH"]),
            "approval_status": random.choice(["PENDING", "APPROVED", "REJECTED", "PAID"]),
            "approved_by": f"EMP{random.randint(1, NUM_EMPLOYEES):06d}",
            "description": fake.sentence()
        })
    return pd.DataFrame(data)

def generate_audit_trail(employees_df, units_df):
    data = []
    modules = ["CUSTOMER", "SAVINGS", "DEPOSIT", "LOAN", "TRANSACTION", "GL", "EXPENSE", "USER_MANAGEMENT"]
    actions = ["CREATE", "UPDATE", "DELETE", "APPROVE", "REJECT", "LOGIN", "LOGOUT", "EXPORT"]
    
    for i in range(1, NUM_AUDIT_TRAIL + 1):
        data.append({
            "audit_id": f"AUD{i:08d}",
            "event_time": fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": f"USR{random.randint(1, 200):04d}",
            "employee_id": random.choice(employees_df['employee_id'].tolist()),
            "unit_id": random.choice(units_df['unit_id'].tolist()),
            "module_name": random.choice(modules),
            "action_type": random.choice(actions),
            "record_id": f"REC{random.randint(1, 5000):06d}",
            "old_value_dummy": "{...}" if random.random() > 0.5 else None,
            "new_value_dummy": "{...}",
            "ip_address_dummy": fake.ipv4(),
            "device_type": random.choice(["WEB", "MOBILE", "BACKOFFICE_PC"]),
            "risk_flag": random.choice(["NORMAL", "SUSPICIOUS", "HIGH_RISK"])
        })
    return pd.DataFrame(data)

def generate_customer_complaints(customers_df, employees_df, units_df):
    data = []
    categories = ["LAYANAN", "PRODUK", "SISTEM_ERROR", "TAGIHAN", "LAINNYA"]
    channels = ["PHONE", "EMAIL", "VISIT", "SOCIAL_MEDIA"]
    
    for i in range(1, NUM_COMPLAINTS + 1):
        comp_date = fake.date_between(start_date="-1y", end_date="today")
        res_date = comp_date + timedelta(days=random.randint(1, 30))
        
        data.append({
            "complaint_id": f"CMP{i:06d}",
            "complaint_date": comp_date.strftime("%Y-%m-%d"),
            "customer_id": random.choice(customers_df['customer_id'].tolist()),
            "employee_id": random.choice(employees_df['employee_id'].tolist()),
            "unit_id": random.choice(units_df['unit_id'].tolist()),
            "complaint_channel": random.choice(channels),
            "complaint_category": random.choice(categories),
            "priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "status": random.choice(["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"]),
            "description": fake.text(max_nb_chars=100),
            "resolution_date": res_date.strftime("%Y-%m-%d") if random.random() > 0.3 else None,
            "resolution_notes": fake.sentence() if random.random() > 0.3 else None,
            "resolution_days": (res_date - comp_date).days if random.random() > 0.3 else None
        })
    return pd.DataFrame(data)

def generate_monthly_snapshot():
    data = []
    for i in range(1, NUM_SNAPSHOTS + 1):
        snapshot_date = (datetime.now().replace(day=1) - timedelta(days=30*i)).strftime("%Y-%m-%d")
        data.append({
            "snapshot_id": f"SNAP{i:04d}",
            "snapshot_date": snapshot_date,
            "total_customers": random.randint(2500, 3000),
            "total_savings_balance": float(random.randint(5000000000, 10000000000)),
            "total_deposit_balance": float(random.randint(2000000000, 5000000000)),
            "total_loan_outstanding": float(random.randint(8000000000, 15000000000)),
            "npl_ratio": round(random.uniform(0.01, 0.08), 4),
            "total_transactions": random.randint(5000, 15000),
            "cash_in": float(random.randint(1000000000, 5000000000)),
            "cash_out": float(random.randint(900000000, 4800000000)),
            "total_operational_expense": float(random.randint(100000000, 500000000)),
            "profit_loss_before_tax": float(random.randint(50000000, 300000000))
        })
    return pd.DataFrame(data)


def main():
    print(f"Generating data for {NUM_CUSTOMERS} customers...")
    
    # 1. Generate core tables
    units_df = generate_operation_units()
    employees_df = generate_employees(units_df)
    customers_df = generate_customers()
    
    # 2. Generate accounts & loans
    savings_df = generate_accounts_savings(customers_df, units_df)
    deposits_df = generate_accounts_deposit(customers_df, units_df)
    loans_df = generate_loans(customers_df, units_df, employees_df)
    
    # 3. Generate child tables
    installments_df = generate_loan_installments(loans_df)
    transactions_df = generate_transactions(savings_df, deposits_df, loans_df, units_df, employees_df)
    collaterals_df = generate_collaterals(loans_df)
    
    # 4. Generate GL & accounting
    gl_accounts_df = generate_gl_accounts()
    gl_journals_df = generate_gl_journals(gl_accounts_df, units_df)
    
    # 5. Generate operational data
    collection_df = generate_collection_activity(loans_df, employees_df)
    expenses_df = generate_expense_operational(units_df)
    audit_df = generate_audit_trail(employees_df, units_df)
    complaints_df = generate_customer_complaints(customers_df, employees_df, units_df)
    snapshots_df = generate_monthly_snapshot()
    
    # Create dictionary mapping
    tables = {
        "01_operation_units": units_df,
        "02_employees": employees_df,
        "03_customers": customers_df,
        "04_accounts_savings": savings_df,
        "05_accounts_deposit": deposits_df,
        "06_loans": loans_df,
        "07_loan_installments": installments_df,
        "08_transactions": transactions_df,
        "09_collateral": collaterals_df,
        "10_gl_accounts": gl_accounts_df,
        "11_gl_journal": gl_journals_df,
        "12_collection_activity": collection_df,
        "13_expense_operational": expenses_df,
        "14_audit_trail": audit_df,
        "15_customer_complaints": complaints_df,
        "16_monthly_snapshot": snapshots_df
    }
    
    # Validation against schema to ensure columns are correct
    for name, df in tables.items():
        base_name = name.split('_', 1)[1]
        req_cols = REQUIRED_COLUMNS.get(base_name)
        if req_cols:
            df = df[req_cols] # Ensure order and presence
            tables[name] = df
            
            # Save to CSV
            csv_path = os.path.join(OUTPUT_DIR, f"{base_name}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Saved {csv_path} ({len(df)} rows)")
    
    # Save to Excel
    print(f"Saving all tables to Excel: {EXCEL_OUTPUT} (This might take a while...)")
    with pd.ExcelWriter(EXCEL_OUTPUT, engine='xlsxwriter') as writer:
        for name, df in tables.items():
            df.to_excel(writer, sheet_name=name, index=False)
            
    print("Dummy data generation completed successfully!")

if __name__ == "__main__":
    main()
