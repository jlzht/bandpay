from fastapi import FastAPI, HTTPException, BackgroundTasks
import requests
import uuid

from app.db.schemas import PaymentRequestCreate

# Esta classe simula um comportamento extremamente simplificado de um gateway de API bancária
class BankAPI:
    def __init__(self):
        self.app = FastAPI(title="Simulated Bank API")  # Cria uma instância FastAPI com um título personalizado.
        self.payments = {}  # Dicionário para armazenar dados fictícios de pagamentos.

        self._setup_routes()  # Configura as rotas da API.

    def _setup_routes(self):

        # URL fictícia para um webhook que será chamado após a validação do pagamento
        WEBHOOK_URL = "http://localhost:8000/transactions/webhook"

        @self.app.post("/generate-payment-link")
        def generate_payment_link(payment: PaymentRequestCreate):
            """Gera um link fictício para pagamento."""
            payment_id = str(uuid.uuid4())  # Gera um ID único para o pagamento.
            payment_url = f"http://localhost:8083/validate-payment/{payment_id}"  # Cria a URL para validação do pagamento.

            # Armazena os dados do pagamento no dicionário interno.
            self.payments[payment_id] = {
                "id": payment_id,
                "user_id": payment.id,
                "amount": payment.amount,
                "status": payment.status,
            }

            # Retorna o ID do pagamento e a URL de validação.
            return {
                "payment_id": payment_id,
                "payment_url": payment_url,
            }

        @self.app.get("/validate-payment/{payment_id}")
        def validate_payment(payment_id: str, background_tasks: BackgroundTasks):
            """Valida o pagamento e envia uma notificação via webhook."""
            if payment_id not in self.payments:  # Verifica se o pagamento existe no dicionário.
                raise HTTPException(status_code=404, detail="Pagamento não encontrado")

            payment_data = self.payments[payment_id]  # Recupera os dados do pagamento.
            payment_data["status"] = "paid"  # Atualiza o status do pagamento para "pago".

            # Adiciona a tarefa de enviar o webhook para execução em segundo plano.
            background_tasks.add_task(
                self._send_webhook, WEBHOOK_URL, payment_data
            )

            # Retorna uma mensagem de sucesso.
            return {"message": "Pagamento validado"}

    def _send_webhook(self, webhook_url: str, payment_data: dict):
        """Envia os dados do pagamento para o webhook."""
        try:
            # Envia uma solicitação POST com os dados do pagamento.
            response = requests.post(webhook_url, json=payment_data)
            response.raise_for_status()  # Verifica se a solicitação foi bem-sucedida.
            print(f"Webhook enviado com sucesso: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Exibe uma mensagem de erro caso a solicitação falhe.
            print(f"Falha ao enviar o webhook: {e}")

    def get_app(self) -> FastAPI:
        """Retorna a instância FastAPI configurada."""
        return self.app
