from fastapi import APIRouter, HTTPException, Depends
from models.transaction_history import TransactionHistory
from config.database import db
from middleware.auth_middleware import get_current_user
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/transaction-history", response_model=TransactionHistory)
async def create_transaction_history(
    transaction: TransactionHistory,
    current_user: str = Depends(get_current_user)
):
    """
    Create a new transaction history entry.
    This endpoint can be used for manual transaction history entries beyond linking accounts or making payments.
    """
    
    # Ensure the transaction is associated with the current user
    transaction.username = current_user
    transaction_dict = transaction.dict()
    
    # Insert the transaction into the database
    result = await db.db.transaction_history.insert_one(transaction_dict)
    transaction_dict["_id"] = str(result.inserted_id)
    return transaction_dict

@router.get("/transaction-history", response_model=List[TransactionHistory])
async def get_transaction_history(current_user: str = Depends(get_current_user)):
    """
    Retrieve all transaction history entries for the current user.
    """
    transactions = []
    async for transaction in db.db.transaction_history.find({"username": current_user}):
        transaction["_id"] = str(transaction["_id"])
        transactions.append(TransactionHistory(**transaction))
    if not transactions:
        raise HTTPException(status_code=404, detail="No transaction history found for this user")
    return transactions

@router.get("/transaction-history/{transaction_id}", response_model=TransactionHistory)
async def get_transaction_by_id(
    transaction_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Retrieve a specific transaction history entry by its ID.
    """
    try:
        transaction = await db.db.transaction_history.find_one(
            {"_id": ObjectId(transaction_id), "username": current_user}
        )
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        transaction["_id"] = str(transaction["_id"])
        return TransactionHistory(**transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid transaction ID")

@router.put("/transaction-history/{transaction_id}", response_model=TransactionHistory)
async def update_transaction_history(
    transaction_id: str,
    transaction: TransactionHistory,
    current_user: str = Depends(get_current_user)
):
    """
    Update a specific transaction history entry by its ID.
    """
    try:
        existing_transaction = await db.db.transaction_history.find_one(
            {"_id": ObjectId(transaction_id), "username": current_user}
        )
        if not existing_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        # Ensure the username remains tied to the current user
        transaction.username = current_user
        update_data = transaction.dict(exclude_unset=True)

        await db.db.transaction_history.update_one(
            {"_id": ObjectId(transaction_id)},
            {"$set": update_data}
        )

        updated_transaction = await db.db.transaction_history.find_one(
            {"_id": ObjectId(transaction_id)}
        )
        updated_transaction["_id"] = str(updated_transaction["_id"])
        return TransactionHistory(**updated_transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid transaction ID")

@router.delete("/transaction-history/{transaction_id}")
async def delete_transaction_history(
    transaction_id: str,
    current_user: str = Depends(get_current_user)
):
    """
    Delete a specific transaction history entry by its ID.
    """
    try:
        result = await db.db.transaction_history.delete_one(
            {"_id": ObjectId(transaction_id), "username": current_user}
        )
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return {"message": "Transaction deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid transaction ID")