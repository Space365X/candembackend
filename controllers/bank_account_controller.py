from fastapi import APIRouter, HTTPException, Depends
from models.bank_account import BankAccount
from config.database import db
from middleware.auth_middleware import get_current_user

router = APIRouter()

@router.post("/bank-account")
async def create_bank_account(bank_account: BankAccount, current_user: str = Depends(get_current_user)):
    bank_account.username = current_user
    await db.db.bank_accounts.insert_one(bank_account.dict())
    return {"message": "Bank account created successfully"}

@router.get("/bank-account")
async def get_bank_account(current_user: str = Depends(get_current_user)):
    bank_account = await db.db.bank_accounts.find_one({"username": current_user})
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return bank_account

@router.put("/bank-account")
async def update_bank_account(bank_account: BankAccount, current_user: str = Depends(get_current_user)):
    await db.db.bank_accounts.update_one(
        {"username": current_user},
        {"$set": bank_account.dict(exclude_unset=True)}
    )
    return {"message": "Bank account updated successfully"}

@router.delete("/bank-account")
async def delete_bank_account(current_user: str = Depends(get_current_user)):
    await db.db.bank_accounts.delete_one({"username": current_user})
    return {"message": "Bank account deleted successfully"}

@router.get("/dashboard")
async def get_dashboard(current_user: str = Depends(get_current_user)):
    bank_account = await db.db.bank_accounts.find_one({"username": current_user})
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return {
        "balance": bank_account["balance"],
        "account_number": bank_account["account_number"],
        "routing_number": bank_account["routing_number"],
        "current_balance": bank_account["current_balance"],
        "last_login":      bank_account["last_login"],
        "username":        bank_account["username"],
        "account_type":    bank_account["account_type"]
    }