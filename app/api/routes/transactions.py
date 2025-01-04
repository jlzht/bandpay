from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.schemas import TransactionCreate


class TransactionRoutes:
    def __init__(self, database, User, Transaction):
        self.User = User = User
        self.Transaction = Transaction
        self.database = database
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        PAYMENT_TYPE = ["credit", "dept"]

        @self.router.post("/")
        def create_transaction(
            tx: TransactionCreate, db: Session = Depends(self.database.get_session)
        ):
            user = db.query(self.User).filter(self.User.id == tx.user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if tx.opt not in PAYMENT_TYPE:  # generalize payment option
                raise HTTPException(status_code=400, detail="Invalid transaction type")
            # Need to register transaction in database table

            new_transaction = self.Transaction(
                user_id=tx.user_id,
                amount=tx.amount,
                opt=tx.opt,
                status="pending"
            )
            db.add(new_transaction)
            db.commit()
            db.refresh(new_transaction)

            new_transaction.status = "approved"
            db.commit()

            user.balance += tx.amount
            
            db.commit()
            db.refresh(user)

            return {
                "transaction_id": new_transaction.id,
                "balance": user.balance,
                "status": new_transaction.status
            }
        
        @self.router.post("/webhook")
        async def validate_payment(transaction_id: int, status: str, db: Session = Depends(self.database.get_session)):
            # Webhook para validar pagamentos
            transaction = db.query(self.Transaction).filter(self.Transaction.id == transaction_id).first()
            if not transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")

            transaction.status = status
            db.commit()
            return {"message": "Transaction status updated"}

        # add  private route used by webhook to validate payment applications
