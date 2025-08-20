from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate
from app.database.db import db
from app.utils.hashing import hashing_password, verify_password
from app.core.auth import create_token
 
router = APIRouter()
 
@router.post("/register")
async def register(user: UserCreate):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hashing_password(user.password)
    new_user = {"email": user.email, "password": hashed}
    result = db.users.insert_one(new_user)                # {"_id": result.inserted_id}
    return result
 
@router.post("/login")
async def login(user: UserCreate):
    db_user = db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token(user.email)
    return {"access_token": token, "token_type": "bearer"}