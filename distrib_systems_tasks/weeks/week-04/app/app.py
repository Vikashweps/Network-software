from fastapi import FastAPI, HTTPException, Header, Body
from schemas import Product, ProductCreate
from typing import List, Optional

app = FastAPI(title="PIZZA TIME")

products_db = [
    Product(id=1, name="Маргарита", description="Томатный соус, моцарелла", price=560.0, stock_quantity=10),
    Product(id=2, name="Пепперони", description="Колбаски пепперони, сыр", price=630.0, stock_quantity=15),
    Product(id=3, name="Четыре сыра", description="Сыр моцарелла, пармезан", price=480.0, stock_quantity=50),
    Product(id=4, name="Гавайская", description="Ветчина, ананасы", price=700.0, stock_quantity=100),
]

reservations_db: dict = {}

@app.get("/")
def root(): 
    return {"status": "ok"}

@app.get("/products/", response_model=List[Product])
def get_products(): 
    return products_db

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((p for p in products_db if p.id == product_id), None)
    if not product: 
        raise HTTPException(404, "Пицца не найдена")
    return product

@app.post("/products/{product_id}/reserve")
def reserve_product(
    product_id: int, 
    data: dict = Body(...), 
    x_order_id: Optional[int] = Header(None, alias="X-Order-Id")  # ✅ Исправлено
):
    if x_order_id is None:
        raise HTTPException(400, "Header 'X-Order-Id' is required")
        
    product = next((p for p in products_db if p.id == product_id), None)
    if not product: 
        raise HTTPException(404, "Пицца не найдена")
    
    quantity = data.get("quantity", 1)
    order_res = reservations_db.setdefault(x_order_id, {})
    
    if order_res.get(product_id, 0) >= quantity:
        return {"status": "already_reserved", "stock": product.stock_quantity}
    
    if product.stock_quantity < quantity:
        raise HTTPException(400, "Недостаточно товара")
    
    product.stock_quantity -= quantity
    order_res[product_id] = quantity
    return {"status": "reserved", "stock": product.stock_quantity}

@app.post("/products/{product_id}/restore")
def restore_product(
    product_id: int, 
    data: dict = Body(...), 
    x_order_id: Optional[int] = Header(None, alias="X-Order-Id")  # ✅ Исправлено
):
    # ✅ Ручная проверка заголовка
    if x_order_id is None:
        raise HTTPException(400, "Header 'X-Order-Id' is required")

    product = next((p for p in products_db if p.id == product_id), None)
    if not product: 
        raise HTTPException(404, "Пицца не найдена")
    
    quantity = data.get("quantity", 1)
    order_res = reservations_db.get(x_order_id, {})
    
    if order_res.get(product_id, 0) == 0:
        return {"status": "already_restored", "stock": product.stock_quantity}
    
    product.stock_quantity += quantity
    del order_res[product_id]
    if not order_res: 
        reservations_db.pop(x_order_id, None)
    
    return {"status": "restored", "stock": product.stock_quantity}

@app.get("/discover")
def discover():
    return {"service": "products-svc", "version": "1.0.0", "port": 8223}