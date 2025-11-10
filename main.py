import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone
from typing import Optional

from database import db, create_document, get_documents
from schemas import Waitlist

app = FastAPI(title="Aurakode API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/waitlist")
def join_waitlist(payload: Waitlist):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    # Unique check
    existing = list(db["waitlist"].find({"email": payload.email}).limit(1))
    if existing:
        return {"ok": True, "message": "Already on the list"}

    create_document("waitlist", {"email": payload.email, "source": payload.source})
    return {"ok": True, "message": "Added"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
