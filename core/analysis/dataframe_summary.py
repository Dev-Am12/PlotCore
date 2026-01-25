import pandas as pd

def load_dataframe(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception:
        return None

def get_basic_summary(df):
    num_rows, num_cols = df.shape
    return {
        "num_rows": num_rows,
        "num_cols": num_cols,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
    }

def get_numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist()