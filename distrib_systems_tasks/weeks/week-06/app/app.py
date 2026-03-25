import uuid
from typing import List, Optional
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# Простая база данных в памяти
devices = {}

# Определяем типы (согласно варианту week-06)
@strawberry.type
class Device:
    id: strawberry.ID
    name: str
    serial: str

@strawberry.input
class CreateDeviceInput:
    name: str
    serial: str

@strawberry.type
class Query:
    @strawberry.field
    def devices(self) -> List[Device]:
        """Получить все устройства"""
        return list(devices.values())
    
    @strawberry.field
    def device(self, id: strawberry.ID) -> Optional[Device]:
        """Получить устройство по ID"""
        return devices.get(id)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def createDevice(self, input: CreateDeviceInput) -> Device:
        """Создать новое устройство"""
        device_id = str(uuid.uuid4())
        device = Device(
            id=device_id,
            name=input.name,
            serial=input.serial
        )
        devices[device_id] = device
        return device

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
    # Порт 8246 согласно варианту week-06
    uvicorn.run(app, host="0.0.0.0", port=8246)