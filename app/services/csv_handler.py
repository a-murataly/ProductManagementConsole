import pandas as pd
import io
from fastapi import UploadFile

async def read_csv(file: UploadFile):
    contents=await file.read()
    df=pd.read_csv(io.StringIO(contents.decode("utf-8")))
    df.columns=df.columns.str.strip()
    required_columns=["Date","City","Store","Category","Sub-category","Brand","Item","Sales qty","Sales value","Sales COGS"]
    if not all(col in df.columns for col in required_columns):
        missing = list(set(required_columns) - set(df.columns))
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    
    return {"rows": df.shape[0], "columns": df.shape[1]}

def decompose(df):
    levels = ["Date", "City", "Category", "Sub-category", "Brand", "Item"]
    combined_cols = []

    debug_output = []

    for i in range(1, len(levels) + 1):
        col_name = "+".join(levels[:i])
        cols = levels[:i]
        debug_output.append(f"Processing: {cols}")

        try:
            df[col_name] = df[cols].astype(str).agg("|".join, axis=1)
        except Exception as e:
            raise ValueError(f"Ошибка при склейке {cols}: {e}")

        combined_cols.append(col_name)

    return df, combined_cols


def calculate_scaling_factors(df, combined_cols):
    scaling_factors=[]

    for i in range(len(combined_cols)-1):
        upper=combined_cols[i]
        lower=combined_cols[i+1]
        upper_count=df[upper].nunique()
        lower_count=df[lower].nunique()
        ratio=round(lower_count/upper_count,2) if upper_count else None

        scaling_factors.append({
            "from": upper,
            "to":lower,
            "unique_in_from": upper_count,
            "unique_in_to": lower_count,
            "scaling_factor": ratio
        })
    return scaling_factors