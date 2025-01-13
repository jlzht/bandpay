from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.schemas import TransactionCreate
from app.db.schemas import TransactionUpdate
from app.api.routes.routes import Routes
import requests
import uuid

class TransactionRoutes(Routes):
    PAYMENT_TYPE = ["money", "transfers"]
    BANK_API_URL = "http://localhost:8083/generate-payment-link"
    def __init__(self, database, User, Transaction):
        self.User = User
        self.Transaction = Transaction
        super().__init__(database)

    def _register_routes(self):

        @self.router.post("/")
        def create_transaction(
            tx: TransactionCreate, db: Session = Depends(self.database.get_session)
        ):
            user = db.query(self.User).filter(self.User.id == tx.user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            if tx.opt not in self.PAYMENT_TYPE:
                raise HTTPException(status_code=400, detail="Invalid transaction type")

            if (tx.opt == "money"):
                new_transaction = self.Transaction(
                    id = str(uuid.uuid4()), user_id=tx.user_id, amount=tx.amount, opt=tx.opt, status="paid"
                )

                db.add(new_transaction)
                db.commit()
                db.refresh(new_transaction)

                user.balance += tx.amount

                db.commit()
                db.refresh(user)

                return {
                    "balance": user.balance,
                }
            else:

                payment_request = {
                    "id": tx.user_id,
                    "amount": tx.amount,
                    "status": "pending",
                }

                response = requests.post(self.BANK_API_URL, json=payment_request,  verify=False)
                if response.status_code != 200:
                    raise HTTPException(status_code=500, detail="Failed to generate payment link")
                payment_data = response.json()

                new_transaction = self.Transaction(
                    id=payment_data["payment_id"], user_id=tx.user_id, amount=tx.amount, opt=tx.opt, status="pending"
                )


                #new_transaction.id = payment_data["payment_id"]

                if not new_transaction.id:
                    raise HTTPException(status_code=500, detail="Failed to generate payment link")



                db.add(new_transaction)
                db.commit()
                #db.refresh(new_transaction)


                #db.commit()
                #db.refresh(new_transaction)

                return {
                    "transaction_id": payment_data["payment_id"],
                    "transaction_link": payment_data["payment_url"],
                }


        @self.router.post("/webhook")
        async def webhook_handler(
            transaction: TransactionUpdate,
            db: Session = Depends(self.database.get_session),
        ):
            """Handle the webhook response and update the transaction status."""
            updated_transaction = (
                db.query(self.Transaction)
                .filter(self.Transaction.id == transaction.id)
                .first()
            )
            if not updated_transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")

            updated_transaction.status = transaction.status

            if transaction.status == "paid":
                updated_user = (
                    db.query(self.User)
                    .filter(self.User.id == updated_transaction.user_id)
                    .first()
                )
                if not updated_user:
                    raise HTTPException(status_code=404, detail="User not found")

                updated_user.balance += transaction.amount
                db.commit()

            db.commit()
            return {"message": "Transaction status updated"}
