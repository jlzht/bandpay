import requests

class Transaction:
    def __init__(self, user_id, valor, api_client):
        self.user_id = user_id
        self.valor = valor
        self.api_client = api_client
    
    def registrar(self):
        """
        Registra uma transação e atualiza o saldo do usuário.
        """
        if not isinstance(self.valor, (int, float)) or self.valor <= 0:
            print("Erro: O valor da recarga precisa ser um número válido e maior que zero.")
            return

        # Primeiro, obtenha o saldo atual do usuário
        saldo_atual = self.consultar_saldo()
        if saldo_atual is None:
            return  # Caso o saldo não seja encontrado, retorna

        # Realiza a transação
        payload = {
            "user_id": self.user_id,
            "amount": self.valor,
            "opt": "money"
        }

        try:
            # Registrar a transação
            response_transaction = self.api_client.post("transactions", payload)
            if response_transaction is None:
                print("Erro ao registrar transação.")
                return

            # Atualizar o saldo
            novo_saldo = saldo_atual + self.valor
            update_payload =novo_saldo
            response_update = self.api_client.put(f"users/{self.user_id}/balance", update_payload)
            
            if response_update is None:
                print("Erro ao atualizar o saldo do usuário.")
                return
            
            print(f"Saldo recarregado com sucesso. Novo saldo: R$ {novo_saldo}")
        
        except requests.exceptions.RequestException as e:
            print(f"Erro ao tentar recarregar saldo: {e}")

    def consultar_saldo(self):
        """
        Retorna o saldo atual do usuário.
        """
        url_balance = f"{self.api_client.api_url}/users/{self.user_id}/balance"
        try:
            response = self.api_client.get(f"users/{self.user_id}")
            if response is None:
                print("Erro: Usuário não encontrado.")
                return None
            return response.get("balance", 0)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar saldo: {e}")
            return None
