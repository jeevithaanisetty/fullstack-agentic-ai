from fastapi import APIRouter, HTTPException,status
from app.models.user import UserCreate
from app.database.db import db
from app.utils.hashing import hashing_password, verify_password
from app.core.auth import create_token
import re
 
router = APIRouter()
 
@router.post("/register")
async def register(user: UserCreate):

    if not re.match(r"[a-z0-9]+@[a-z]+\.(com)",user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email must be a valid email address")
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$",user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="password should contain atleast 8 letters which include one capital,one small,one digit and atleast one special character")
    
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hashing_password(user.password)
    new_user = {"email": user.email, "password": hashed}
    result = db.users.insert_one(new_user)                # {"_id": result.inserted_id}
    return "user registered successfully"
 
@router.post("/login")
async def login(user: UserCreate):
    db_user = db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token(user.email)
    return {"access_token": token, "token_type": "bearer"}