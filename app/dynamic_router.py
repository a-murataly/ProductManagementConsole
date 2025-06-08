from fastapi import APIRouter
from pydantic import create_model
from typing import Dict, Callable, Any
from app.calculations import calculations

router = APIRouter()

for name, item in calculations.items():
    func: Callable = item["func"]
    args: list[str] = item["args"]
    description: str = item.get("description", "")

    # Создаём Pydantic-модель динамически
    fields: Dict[str, tuple] = {arg: (float, ...) for arg in args}
    InputModel = create_model(f"{name}_Input", **fields)

    # Создаём endpoint-функцию
    def make_endpoint(func: Callable) -> Callable:
        def endpoint(input_data: InputModel):
            kwargs = input_data.dict()
            return {"result": func(**kwargs)}
        return endpoint

    endpoint_func = make_endpoint(func)

    # Регистрируем маршрут
    router.post(f"/{name}", summary=description)(endpoint_func)
