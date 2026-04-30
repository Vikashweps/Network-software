import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Notifications Service")

class NotificationCreate(BaseModel):
    message: str = Field(..., max_length=500)
    channel: str = Field(..., pattern="^(email|sms|telegram)$")
    recipient: str = Field(..., max_length=100)

class Notification(NotificationCreate):
    id: int
    created_at: int
    status: str = "pending"

notifications_db = []
id_counter = 1

@app.post("/notifications/", response_model=Notification, status_code=201)
async def create_notification(notif: NotificationCreate):
    global id_counter
    new = Notification(
        id=id_counter,
        created_at=int(time.time()),
        status="pending",
        **notif.model_dump()
    )
    notifications_db.append(new)
    id_counter += 1
    return new

@app.get("/notifications/", response_model=List[Notification])
async def get_notifications(channel: Optional[str] = None):
    if channel:
        return [n for n in notifications_db if n.channel == channel]
    return notifications_db

@app.get("/discover")
async def discover():
    return {
        "service": "notifications-svc-s16",  
        "port": 8131,                         
        "endpoints": ["GET /notifications/", "POST /notifications/"]
    }

if __name__ == "__main__":
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8131))   
    uvicorn.run(app, host=host, port=port)