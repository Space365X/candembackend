from pydantic import BaseModel
from typing import Optional

class BankAccount(BaseModel):
    username: str
    account_type: str
    last_login: str
    account_number: str
    routing_number: str
    balance: str
    current_balance: str
