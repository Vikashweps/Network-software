# app/schemas.py
from pydantic import BaseModel, Field

class SessionBase(BaseModel):
    user_id: int
    ip: str = Field(..., description="IP-адрес клиента")
    duration: int = Field(..., gt=0, description="Длительность в минутах")

class SessionCreate(SessionBase): pass
class Session(SessionBase):
    id: int
    status: str = "active"