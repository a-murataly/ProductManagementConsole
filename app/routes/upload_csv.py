from fastapi import APIRouter, UploadFile, File
from app.services.csv_handler import read_csv, decompose, calculate_scaling_factors

router=APIRouter()

@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        df = await read_csv(file)
        df, combined_cols = decompose(df)
        scaling = calculate_scaling_factors(df, combined_cols)

        # временно логируем
        print("✅ Scaling factors:", scaling)

        return {"scaling_factors": scaling}
    except Exception as e:
        print("❌ Ошибка:", str(e))
        return {"error": str(e)}