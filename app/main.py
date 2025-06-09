from fastapi import FastAPI
from app.routes import upload_csv

app = FastAPI()

app.include_router(upload_csv.router)