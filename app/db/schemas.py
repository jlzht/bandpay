from pydantic import BaseModel


class UserCreate(BaseModel):
    id: str
    name: str
    status: str

class TransactionCreate(BaseModel):
    user_id: str
    opt: str
    amount: float

class PaymentRequestCreate(BaseModel):
    id: str
    amount: float
    status: str

class TransactionUpdate(BaseModel):
    id: str
    amount: float
    status: str
