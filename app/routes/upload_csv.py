from fastapi import APIRouter, UploadFile, File

router=APIRouter()
@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size_bytes": len(contents)}