from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes import upload_csv

app = FastAPI()

# Подключаем маршруты
app.include_router(upload_csv.router)

# Указываем путь к шаблонам
templates = Jinja2Templates(directory="app/templates")

# Отображаем главную страницу
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})