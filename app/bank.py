from fastapi import FastAPI, HTTPException, BackgroundTasks
import requests
import uuid

from app.db.schemas import PaymentRequestCreate


# This class simulates a extremely simplified behavior of a bank API Gateway
class BankAPI:
    def __init__(self):
        self.app = FastAPI(title="Simulated Bank API")
        self.payments = {}

        self._setup_routes()

    def _setup_routes(self):

        WEBHOOK_URL = "http://localhost:8000/transactions/webhook"

        @self.app.post("/generate-payment-link")
        def generate_payment_link(payment: PaymentRequestCreate):
            """Generate a fictional payment link."""
            payment_id = str(uuid.uuid4())
            payment_url = f"http://localhost:8083/validate-payment/{payment_id}"

            self.payments[payment_id] = {
                "id": payment_id,
                "user_id": payment.id,
                "amount": payment.amount,
                "status": payment.status,
            }

            return {
                    "payment_id": payment_id,
                    "payment_url": payment_url,
            }

        @self.app.get("/validate-payment/{payment_id}")
        def validate_payment(payment_id: str, background_tasks: BackgroundTasks):
            """Validate the payment and send webhook notification."""
            if payment_id not in self.payments:
                raise HTTPException(status_code=404, detail="Payment not found")

            payment_data = self.payments[payment_id]
            payment_data["status"] = "paid"

            background_tasks.add_task(
                self._send_webhook, WEBHOOK_URL, payment_data
            )

            return {"message": "Payment validated"}

    def _send_webhook(self, webhook_url: str, payment_data: dict):
        """Send payment data to the webhook."""
        try:
            response = requests.post(webhook_url, json=payment_data)
            response.raise_for_status()
            print(f"Webhook sent successfully: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send webhook: {e}")

    def get_app(self) -> FastAPI:
        return self.app
