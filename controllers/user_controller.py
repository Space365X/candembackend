from fastapi import APIRouter, HTTPException, Depends
from models.user import User,  OTPVerify
from config.database import db
from utils.auth import get_password_hash
from middleware.auth_middleware import get_current_user
from utils.otp_generator import generate_otp
from utils.redis_helper import redis_helper

router = APIRouter()

@router.post("/register")
async def register(user: User):
    existing_user = await db.db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user_dict["password"])
    await db.db.users.insert_one(user_dict)
    
    otp = generate_otp()
    redis_helper.set_otp(user.username, otp)
    
    return {"message": "User registered successfully", "otp": otp}



@router.post("/verify-otp")
async def verify_otp(verify_data: OTPVerify):
    stored_otp = redis_helper.get_otp(verify_data.username)
    if not stored_otp or stored_otp != verify_data.otp:
        raise HTTPException(status_code=422, detail="Invalid or expired OTP")  # Changed to 422 for clarity
    
    redis_helper.delete_otp(verify_data.username)
    return {"message": "OTP verified successfully"}
@router.get("/user")
async def get_user(current_user: str = Depends(get_current_user)):
    user = await db.db.users.find_one({"username": current_user})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/user")
async def update_user(user: User, current_user: str = Depends(get_current_user)):
    await db.db.users.update_one(
        {"username": current_user},
        {"$set": user.dict(exclude_unset=True)}
    )
    return {"message": "User updated successfully"}

@router.delete("/user")
async def delete_user(current_user: str = Depends(get_current_user)):
    await db.db.users.delete_one({"username": current_user})
    return {"message": "User deleted successfully"}