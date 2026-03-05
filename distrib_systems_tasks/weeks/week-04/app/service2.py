from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from saga import PizzaSaga
import requests 

app = FastAPI(title="Gateway Service")


# МОДЕЛИ
class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderResponse(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    status: str


# ХРАНИЛИЩЕ ЗАКАЗОВ
orders_db = []
next_order_id = 1

# URL сервиса пицц 
APP_URL = "http://products-svc-s16:8223"

@app.get("/other")
async def get_other():
    return {"service": "gateway-svc", "project_code": "sessions-s16", "status": "ok"}

@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate):
    """
    Создать заказ через Сагу.
    Если оплата не пройдёт — сработает компенсация.
    """
    global next_order_id
    
    order_id = next_order_id
    next_order_id += 1
    
    # Создаём и запускаем Сагу
    saga = PizzaSaga(order_id, order.product_id, order.quantity, APP_URL)
    saga.execute(orders_db)
    
    # Возвращаем результат
    for o in orders_db:
        if o["order_id"] == order_id:
            return o
    
    return {"order_id": order_id, "product_id": order.product_id, "quantity": order.quantity, "status": "ERROR"}


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    """Получить заказ по ID"""
    order = next((o for o in orders_db if o["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@app.get("/")
async def root():
    return {
        "service": "gateway-svc",
        "project_code": "sessions-s16",
        "status": "ok"
    }


@app.get("/discover")
async def discover():
    """Информация о сервисе"""
    return {
        "service": "gateway-svc",
        "project_code": "sessions-s16",
        "version": "1.0.0",
        "endpoints": [
            "GET /",
            "GET /discover",
            "POST /orders/",
            "GET /orders/{id}"
        ]
    }