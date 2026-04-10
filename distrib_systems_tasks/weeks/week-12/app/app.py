# app/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="shipments-svc-s16")

shipments_db = []
next_id = 1

class ShipmentCreate(BaseModel):
    origin: str
    destination: str
    tracking: str  # extra_field из варианта
    weight: float = Field(..., gt=0)

class Shipment(ShipmentCreate):
    id: int
    status: str = "created"

@app.get("/health")
def health():
    return {"status": "ok", "service": "shipments-svc-s16"}

@app.post("/api/shipments", response_model=Shipment, status_code=201)
def create_shipment(shipment: ShipmentCreate):
    global next_id
    s = Shipment(id=next_id, **shipment.model_dump())
    shipments_db.append(s)
    next_id += 1
    return s

@app.get("/api/shipments", response_model=List[Shipment])
def list_shipments():
    return shipments_db

@app.get("/api/shipments/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: int):
    s = next((x for x in shipments_db if x.id == shipment_id), None)
    if not s:
        raise HTTPException(status_code=404, detail="Доставка не найдена")
    return s

@app.put("/api/shipments/{shipment_id}", response_model=Shipment)
def update_shipment(shipment_id: int, shipment: ShipmentCreate):
    s = next((x for x in shipments_db if x.id == shipment_id), None)
    if not s:
        raise HTTPException(status_code=404, detail="Доставка не найдена")
    s.origin = shipment.origin
    s.destination = shipment.destination
    s.tracking = shipment.tracking
    s.weight = shipment.weight
    return s

@app.delete("/api/shipments/{shipment_id}", status_code=204)
def delete_shipment(shipment_id: int):
    global shipments_db
    s = next((x for x in shipments_db if x.id == shipment_id), None)
    if not s:
        raise HTTPException(status_code=404, detail="Доставка не найдена")
    shipments_db = [x for x in shipments_db if x.id != shipment_id]
    return None