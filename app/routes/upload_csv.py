from fastapi import APIRouter, UploadFile, File
from app.services.csv_handler import read_csv, decompose, calculate_scaling_factors

router=APIRouter()

@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        df = await read_csv(file)
        df_baseline = df.copy()

        df, combined_cols = decompose(df)
        df_baseline,_=decompose(df_baseline)

        filtered = calculate_scaling_factors(df, combined_cols)
        baseline = calculate_scaling_factors(df_baseline, combined_cols)
        
        return {
            "filtered_factors": filtered,
            "baseline_factors": baseline
            }
    except Exception as e:        
        return {"error": str(e)}