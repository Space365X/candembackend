from fastapi import APIRouter, HTTPException, Depends
from models.user import UserLogin
from utils.auth import verify_password, create_access_token
from config.database import db

router = APIRouter()

@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.db.users.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}