import pandas as pd
import streamlit as st

def convert_df_to_csv(df: pd.DataFrame) -> str:
    """Convert dataframe to CSV string for download"""
    return df.to_csv(index=False).encode('utf-8')
    
def apply_download_button(df: pd.DataFrame, filename: str, label: str = "Download Data as CSV"):
    if not df.empty:
        export_df = df
        if st.session_state.get('toggle_masking', True):
            export_df = mask_dataframe(df)
        csv = convert_df_to_csv(export_df)
        st.download_button(
            label=label,
            data=csv,
            file_name=filename,
            mime='text/csv',
        )

def mask_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty: return df
    df_copy = df.copy()
    
    if 'full_name' in df_copy.columns:
        def mask_name(x):
            if not isinstance(x, str): return x
            parts = x.split(' ')
            if len(parts) > 1: return parts[0] + ' ' + parts[1][0] + '***'
            return x[:3] + '***'
        df_copy['full_name'] = df_copy['full_name'].apply(mask_name)
        
    if 'account_id' in df_copy.columns:
        df_copy['account_id'] = df_copy['account_id'].apply(lambda x: str(x)[:3] + '***' + str(x)[-3:] if pd.notnull(x) else x)
        
    if 'customer_id' in df_copy.columns:
        df_copy['customer_id'] = df_copy['customer_id'].apply(lambda x: str(x)[:3] + '***' + str(x)[-3:] if pd.notnull(x) else x)
        
    if 'phone_number' in df_copy.columns:
        df_copy['phone_number'] = df_copy['phone_number'].apply(lambda x: str(x)[:4] + '***' + str(x)[-4:] if pd.notnull(x) else x)
        
    if 'nik' in df_copy.columns:
        df_copy['nik'] = df_copy['nik'].apply(lambda x: str(x)[:4] + '***' + str(x)[-4:] if pd.notnull(x) else x)
        
    return df_copy

# Monkey patch st.dataframe
_original_dataframe = st.dataframe
def patched_dataframe(data, *args, **kwargs):
    if st.session_state.get('toggle_masking', True):
        if isinstance(data, pd.DataFrame):
            data = mask_dataframe(data)
    return _original_dataframe(data, *args, **kwargs)
st.dataframe = patched_dataframe

def check_password():
    """Returns `True` if the user had a correct password."""
    def password_entered():
        username = st.session_state.get("username")
        password = st.session_state.get("password")
        
        if st.session_state.get("password_correct"):
            return
            
        if username == "moleng" and password == "hangus":
            st.session_state["password_correct"] = True
            st.session_state.pop("password", None)
            st.session_state.pop("username", None)
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("### 🔒 Login Diperlukan")
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password", on_change=password_entered)
        st.button("Login", on_click=password_entered)
        
        if "password_correct" in st.session_state and st.session_state["password_correct"] is False:
            st.error("😕 Username atau password salah.")
        return False
        
    # If logged in, inject Sidebar Toggle
    st.sidebar.markdown("---")
    st.sidebar.toggle("🔒 Data Masking (POJK)", value=True, key="toggle_masking")
    return True
