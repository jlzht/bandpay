from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.models import Transaction
from app.db.models import User
from app.db.schemas import TransactionCreate

class TransactionRoutes:
    def __init__(self, database_cb):
        self.database_cb = database_cb
        self.router = APIRouter()
        # self.transaction_service = TransactionService()
        self._register_routes()

    def _register_routes(self):
        @self.router.post("/")
        def create_transaction(tx: TransactionCreate, db: Session = Depends(self.database_cb)):
            user = db.query(User).filter(User.id == tx.user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if tx.opt not in ["credit", "dept"]: # generalize payment option
                raise HTTPException(status_code=400, detail="Invalid transaction type")

            # this should handle transactions validations
            # transaction = self.transaction_service.create_transaction(tx, user)
            # background_tasks.add_task(self.transaction_service.simulate_webhook, transaction.id)
            
            return {"transaction_id": transaction.id, "status": transaction.status}
