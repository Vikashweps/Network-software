from fastapi import FastAPI, HTTPException 
from typing import List
from schemas import Product, ProductCreate


app = FastAPI(title="PIZZA TIME")

# Имитация базы данных
products_db = [
    Product(id=1, name="Маргарита", description="Основа с томатным соусом, свежей моцареллой, базиликом и оливковым маслом", price=560.0, stock_quantity=10),
    Product(id=2, name="Пепперони", description="Классическая пицца с пряными колбасками пепперони и большим количеством сыра", price=630.0, stock_quantity=15),
    Product(id=3, name="Четыре сыра", description="Белая пицца (без томатного соуса), включающая горгонзолу, моцареллу, пармезан и эмменталь/фонтину", price=480.0, stock_quantity=50),
    Product(id=4, name="Гавайская", description="Ветчина, сыр моцарелла и ананасы", price=700.0, stock_quantity=100),
]
id_counter = 5

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в PIZZA TIME!"}

@app.post("/products/", response_model=Product, status_code=201)
async def create_product(product: ProductCreate):
    global id_counter
    new_product = Product(id=id_counter, **product.model_dump())
    products_db.append(new_product)
    id_counter += 1
    return new_product

@app.get("/products/", response_model=List[Product])
async def get_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Пицца не найдена")
    return product


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductCreate):
    existing = next((p for p in products_db if p.id == product_id), None)
    if not existing:
        raise HTTPException(status_code=404, detail="Пицца не найдена")
    
    existing.name = product.name
    existing.description = product.description
    existing.price = product.price
    existing.stock_quantity = product.stock_quantity
    return existing

@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int):
    global products_db
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Пицца не найдена")
    products_db = [p for p in products_db if p.id != product_id]
    return None