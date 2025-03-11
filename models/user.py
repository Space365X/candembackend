from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    phone_number: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class OTPVerify(BaseModel):
    username: str
    otp: str