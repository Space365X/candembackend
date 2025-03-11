from sqlite3 import Date
from pydantic import BaseModel
from typing import Optional

class TransactionHistory(BaseModel):
    username: str
    #user_id: str
    amount: float
    transaction_type: str
    #bank_numbers: str
    #routing_numbers: Optional[str] = None
    account_balance: str
    date_time: str
