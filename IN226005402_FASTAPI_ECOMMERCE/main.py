from fastapi import FastAPI, Query

app = FastAPI()  # <- THIS is what uvicorn is looking for

# Sample products list
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

# ── Task 1: Filter products by price/category ──
@app.get("/products/filter")
def filter_products(
    min_price: int = Query(None, description="Minimum price"),
    max_price: int = Query(None, description="Maximum price"),
    category: str = Query(None, description="Category filter")
):
    result = products
    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]
    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]
    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]
    return result

# ── Task 2: Get only the price of a product ──
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"name": product["name"], "price": product["price"]}
    return {"error": "Product not found"}
@app.get("/products/names")
def get_product_names():
    return [p["name"] for p in products]
@app.get("/products/{product_id}/stock")
def check_stock(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {"name": product["name"], "in_stock": product["in_stock"]}
    return {"error": "Product not found"}
@app.post("/products/add")
def add_product(
    name: str = Query(..., description="Product name"),
    price: int = Query(..., description="Product price"),
    category: str = Query(..., description="Product category"),
    in_stock: bool = Query(..., description="Is product in stock?")
):
    new_id = max([p["id"] for p in products]) + 1
    new_product = {
        "id": new_id,
        "name": name,
        "price": price,
        "category": category,
        "in_stock": in_stock
    }
    products.append(new_product)
    return {"message": "Product added successfully", "product": new_product}