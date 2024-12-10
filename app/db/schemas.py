from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    id: int
    name: str
    status: str

class TransactionCreate(BaseModel):
    user_id: int
    opt: str
    amount: float

class TransactionWebhook(BaseModel):
    transaction_id: int
    status: str
