import uuid
from typing import List
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Простая база данных в памяти
products = {}

# Определяем типы
@strawberry.type
class Product:
    id: strawberry.ID
    name: str
    price: float
    in_stock: bool

@strawberry.input
class ProductInput:
    name: str
    price: float
    in_stock: bool = True

@strawberry.type
class Query:
    @strawberry.field
    def products(self) -> List[Product]:
        """Получить все продукты"""
        return list(products.values())

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_product(self, input: ProductInput) -> Product:
        """Создать новый продукт"""
        product_id = str(uuid.uuid4())
        product = Product(
            id=product_id,
            name=input.name,
            price=input.price,
            in_stock=input.in_stock
        )
        products[product_id] = product
        return product

# Создаем схему
schema = strawberry.Schema(query=Query, mutation=Mutation)

# FastAPI приложение
app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")

@app.get("/")
async def root():
    return {"message": "GraphQL API работает", "endpoint": "/graphql"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8223)
