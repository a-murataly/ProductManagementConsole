from fastapi import APIRouter, UploadFile, File, Form
from app.services.csv_handler import read_csv, decompose, calculate_scaling_factors
from app.services.csv_handler import unique_values

router=APIRouter()

@router.post("/upload_csv")
async def upload_csv(
    file: UploadFile = File(...),
    brand: str = Form(...)
    ):
    try:
        df = await read_csv(file)        
        df_filtered=df[df["Brand"]==brand]
        df_baseline = df.copy()
        all_filters = unique_values(df)

        df_filtered, combined_cols = decompose(df_filtered)
        df_baseline,_=decompose(df_baseline)

        filtered = calculate_scaling_factors(df_filtered, combined_cols)
        baseline = calculate_scaling_factors(df_baseline, combined_cols)
        
        return {
            "filtered_factors": filtered,
            "baseline_factors": baseline,
            "filters": all_filters
        }
    except Exception as e:        
        return {"error": str(e)}