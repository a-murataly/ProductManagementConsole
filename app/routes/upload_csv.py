from fastapi import APIRouter, UploadFile, File
from app.services.csv_handler import read_csv, decompose, calculate_scaling_factors

router=APIRouter()
@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    df=await read_csv(file)
    df,combined_cols=decompose(df)
    scaling=calculate_scaling_factors(df,combined_cols)
    return {"scaling factors:": scaling}