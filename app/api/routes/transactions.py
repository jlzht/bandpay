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
        # Endpoint para criar uma transação
        @self.router.post("/")
        def create_transaction(
            tx: TransactionCreate, db: Session = Depends(self.database.get_session)
        ):
            # Consulta o usuário no banco
            user = db.query(self.User).filter(self.User.id == tx.user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Verifica se a transação é de um tipo válido
            if tx.opt not in self.PAYMENT_TYPE:
                raise HTTPException(status_code=400, detail="Invalid transaction type")

            # Processa o tipo "money" (dinheiro)
            if tx.opt == "money":
                new_transaction = self.Transaction(
                    id=str(uuid.uuid4()), user_id=tx.user_id, amount=tx.amount, opt=tx.opt, status="paid"
                )

                db.add(new_transaction)
                db.commit()
                db.refresh(new_transaction)

                # Atualiza o saldo do usuário
                user.balance += tx.amount
                db.commit()
                db.refresh(user)

                return {
                    "balance": user.balance,
                }

            # Processa o tipo "transfers" (pagamento externo)
            else:
                payment_request = {
                    "id": tx.user_id,
                    "amount": tx.amount,
                    "status": "pending",
                }

                # Faz a solicitação para o serviço de pagamento externo
                try:
                    response = requests.post(self.BANK_API_URL, json=payment_request, verify=False)
                    response.raise_for_status()  # Lança um erro para status não 2xx
                except requests.exceptions.RequestException as e:
                    raise HTTPException(status_code=500, detail=f"Failed to generate payment link: {e}")
                
                payment_data = response.json()

                # Cria uma nova transação com base na resposta do pagamento
                new_transaction = self.Transaction(
                    id=payment_data["payment_id"], user_id=tx.user_id, amount=tx.amount, opt=tx.opt, status="pending"
                )

                db.add(new_transaction)
                db.commit()

                return {
                    "transaction_id": payment_data["payment_id"],
                    "transaction_link": payment_data["payment_url"],
                }

        # Endpoint para receber o webhook
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

            # Atualiza o saldo do usuário quando a transação for concluída (status 'paid')
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
