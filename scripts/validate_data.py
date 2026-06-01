import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.validator import DataValidator

RAW_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'bpr_simulasi_dummy_dataset.xlsx')
REPORT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'rejected', 'validation_report.xlsx')

def main():
    print("Starting data validation...")
    validator = DataValidator(RAW_FILE)
    report_df = validator.validate_all()
    
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    report_df.to_excel(REPORT_FILE, index=False)
    
    fails = report_df[report_df['status'] == 'FAIL']
    
    print("\n=== VALIDATION SUMMARY ===")
    print(f"Total Checks: {len(report_df)}")
    print(f"Passed: {len(report_df) - len(fails)}")
    print(f"Failed: {len(fails)}")
    
    if not fails.empty:
        print("\nFAILURES:")
        for _, row in fails.iterrows():
            print(f"- {row['table']} | {row['check_type']}: {row['message']}")
            
    print(f"\nReport saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()
