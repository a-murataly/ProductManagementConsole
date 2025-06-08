from fastapi import FastAPI
from app.schemas import CategoryShareInput
app=FastAPI()

@app.get("/")
def root():
  return {"message": "Product Management Console is running!"}

@app.post("/category_share")
def calculate_share(data: CategoryShareInput):
  share=data.product_sales_value_input/data.category_sales_value_input
  return {"share": round(share,3)}