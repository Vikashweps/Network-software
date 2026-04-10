# app/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import uuid

app = FastAPI(title="sessions-svc-s16")

sessions_db = []
next_id = 1

class SessionCreate(BaseModel):
    user_id: int
    ip: str  # extra_field из варианта
    duration: int = Field(..., gt=0, description="Длительность в минутах")

class Session(SessionCreate):
    id: int
    status: str = "active"

@app.get("/health")
def health():
    return {"status": "ok", "service": "sessions-svc-s16"}

@app.post("/api/sessions", response_model=Session, status_code=201)
def create_session(sess: SessionCreate):
    global next_id
    s = Session(id=next_id, **sess.model_dump())
    sessions_db.append(s)
    next_id += 1
    return s

@app.get("/api/sessions", response_model=List[Session])
def list_sessions():
    return sessions_db

@app.get("/api/sessions/{session_id}", response_model=Session)
def get_session(session_id: int):
    s = next((x for x in sessions_db if x.id == session_id), None)
    if not s:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    return s

@app.delete("/api/sessions/{session_id}", status_code=204)
def delete_session(session_id: int):
    global sessions_db
    s = next((x for x in sessions_db if x.id == session_id), None)
    if not s:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    sessions_db = [x for x in sessions_db if x.id != session_id]
    return None