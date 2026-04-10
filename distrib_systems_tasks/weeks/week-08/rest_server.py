
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import time
import uvicorn

app = FastAPI()

likes_db = []
current_id = 1

class LikeCreate(BaseModel):
    author: str
    target: str

class Like(BaseModel):
    id: int
    author: str
    target: str
    created_at: int

@app.post("/likes", response_model=Like)
def create_like(like: LikeCreate):
    global current_id
    new_like = Like(id=current_id, author=like.author, target=like.target, created_at=int(time.time()))
    likes_db.append(new_like)
    current_id += 1
    return new_like

@app.get("/likes", response_model=List[Like])
def get_likes():
    return likes_db

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)