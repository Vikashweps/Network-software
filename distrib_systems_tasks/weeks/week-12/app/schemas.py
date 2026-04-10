# app/schemas.py
from pydantic import BaseModel, Field

class ShipmentBase(BaseModel):
    origin: str
    destination: str
    tracking: str = Field(..., description="Трекинг-номер")
    weight: float = Field(..., gt=0, description="Вес в кг")

class ShipmentCreate(ShipmentBase):
    pass

class Shipment(ShipmentBase):
    id: int
    status: str = "created"