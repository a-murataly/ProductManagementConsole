def category_share(product_sales: float, category_sales: float) -> float:
    return round(product_sales/category_sales, 3)

calculations = {
    "category_share": {
        "func": category_share,
        "args": ["product_sales", "category_sales"],
        "description": "Calculates share of a product in category"
    }
}