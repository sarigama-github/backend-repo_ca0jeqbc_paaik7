from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr
from typing import Optional
from datetime import datetime

from database import db, create_document
from schemas import Waitlist

app = FastAPI(title="Aurakode API", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.post("/waitlist")
async def join_waitlist(payload: Waitlist):
    # ensure uniqueness by email
    existing = await db["waitlist"].find_one({"email": payload.email})
    if existing:
        return {"ok": True, "message": "Already on the list"}

    doc = await create_document("waitlist", payload.dict())
    if not doc:
        raise HTTPException(status_code=500, detail="Failed to join waitlist")
    return {"ok": True}
