from pydantic import BaseModel, Field
from typing import Optional



class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название продукта")
    description: Optional[str] = Field(None, max_length=500, description="Описание продукта")
    price: float = Field(..., gt=0, description="Цена в рублях")
    stock_quantity: int = Field(..., ge=0, description="Количество на складе")

class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
