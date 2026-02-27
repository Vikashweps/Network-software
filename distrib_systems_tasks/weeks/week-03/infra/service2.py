from fastapi import FastAPI
from typing import List

app = FastAPI(title="Other Service")
@app.get("/other")
async def get_other():
    return {"service": "other-svc", "status": "ok", "message": "Mock endpoint"}

@app.get("/")
async def root():
    return {"message": "Other service is running"}