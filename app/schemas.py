from pydantic import BaseModel

class CategoryShareInput(BaseModel):
    product_sales_value_input: float
    category_sales_value_input: float