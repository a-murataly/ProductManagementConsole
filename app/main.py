from fastapi import FastAPI
from app.dynamic_router import router

app = FastAPI()

app.include_router(router)