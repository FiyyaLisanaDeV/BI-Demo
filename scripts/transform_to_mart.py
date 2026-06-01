import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.transformer import DataTransformer

RAW_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'bpr_simulasi_dummy_dataset.xlsx')
MART_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'mart')
MART_EXCEL = os.path.join(MART_DIR, 'bpr_simulasi_mart.xlsx')

def main():
    print("Starting data transformation to Data Mart...")
    os.makedirs(MART_DIR, exist_ok=True)
    
    transformer = DataTransformer(RAW_FILE)
    marts = transformer.build_all_marts()
    
    with pd.ExcelWriter(MART_EXCEL, engine='xlsxwriter') as writer:
        for name, df in marts.items():
            if not df.empty:
                # Save to CSV
                csv_path = os.path.join(MART_DIR, f"{name}.csv")
                df.to_csv(csv_path, index=False)
                
                # Convert period to string for excel
                for col in df.select_dtypes(include=['period[M]']).columns:
                    df[col] = df[col].astype(str)
                    
                # Save to Excel
                df.to_excel(writer, sheet_name=name, index=False)
                print(f"Created {name} with {len(df)} rows")
                
    print(f"\nAll Data Marts successfully created at: {MART_DIR}")

if __name__ == "__main__":
    main()
