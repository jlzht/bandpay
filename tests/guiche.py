import requests

class Guiche:
    def __init__(self, api_url):
        self.api_url = api_url

    def consultar_saldo(self, user_id):
        """
        Consulta o saldo de um usuário específico.
        """
        url = f"{self.api_url}/users/{user_id}/balance"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Levanta um erro para status 4xx/5xx
            return response.json().get("balance")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar saldo: {e}")
            return None
    
    def recarregar_saldo(self, user_id, valor):
        """
        Registra uma transação para o usuário e atualiza o saldo.
        """
        url = f"{self.api_url}/transactions"
        url_balance = f"{self.api_url}/users/{user_id}"  # Usando o ID do usuário para buscar o saldo correto
        
        try:
            response_balance = requests.get(url_balance)
            response_balance.raise_for_status()
            user = response_balance.json()  # Obtendo os dados do usuário

            # Payload para criar a transação
            payload = {
                "user_id": user_id,
                "amount": valor,
                "opt": "money"  # Tipo de transação
            }

            # Solicitação para registrar a transação
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Levanta um erro para status 4xx/5xx

            # Atualizar o saldo do usuário
            novo_saldo = user["balance"] + valor
            print(f"Saldo recarregado com sucesso. Novo saldo: R$ {novo_saldo}")
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Erro ao registrar transação: {e}")
            return None
    
    def verifica_catraca(self, user_id):
        """
        Verifica se o usuário tem crédito suficiente para passar pela catraca.
        Caso tenha, decrementa R$ 5 do saldo e libera o acesso.
        Caso contrário, avisa que o saldo é insuficiente.
        """
        url_balance = f"{self.api_url}/users/{user_id}"
        
        try:
            response_balance = requests.get(url_balance)
            response_balance.raise_for_status()

            user = response_balance.json()
            
            # Garantir que o saldo seja um float
            saldo_atual = float(user["balance"])
            
            if saldo_atual >= 5:
                novo_saldo = saldo_atual - 5  # Decrementa R$ 5 do saldo

                url_update_balance = f"{self.api_url}/users/{user_id}/update_balance"
                # Enviar o novo saldo corretamente no formato de dicionário
                payment= novo_saldo

                response_update_balance = requests.patch(url_update_balance, json=payment)
                response_update_balance.raise_for_status()

                print(f"Passagem liberada! Novo saldo: R$ {novo_saldo}")
                return "Liberado"
            else:
                print("Erro: Saldo insuficiente para passar pela catraca.")
                return "Saldo insuficiente"

        except requests.exceptions.RequestException as e:
            print(f"Erro ao verificar catraca: {e}")
            return None

    def altera_saldo(self, user_id, valor):
        """
        Recarrega o saldo de um usuário.
        """
        url = f"{self.api_url}/users/{user_id}/balance/"
        payload = valor  
        response = requests.put(url, json=payload)
        if response.status_code == 200:
            print(f"Saldo recarregado com sucesso. Novo saldo: R$ {valor}")
        else:
            print(f"Erro ao recarregar saldo: {response.status_code}")


    def listar_usuarios(self):
        """
        Lista todos os usuários cadastrados.
        """
        url = f"{self.api_url}/users/"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Levanta erro para status inválido
            users = response.json()
            if users:
                print("Usuários cadastrados:")
                for user in users:
                    print(f"ID: {user['id']}, Nome: {user['name']}, Status: {user['status']}, Saldo: {user['balance']}")
            else:
                print("Nenhum usuário encontrado.")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao listar usuários: {e}")

    def pesquisar_usuario(self, user_id):
        """
        Pesquisa um usuário pelo ID.
        """
        url = f"{self.api_url}/users/{user_id}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            user = response.json()
            print(f"Usuário encontrado: ID: {user['id']}, Nome: {user['name']}, Status: {user['status']}, Saldo: R$ {user['balance']:.2f}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao pesquisar usuário: {e}")


# Menu de interação com o guichê
def menu():
    api_url = "http://127.0.0.1:8000"  # URL base da API
    guiche = Guiche(api_url)
    
    while True:
        print("\nMenu do Guichê:")
        print("1. Listar Usuários")
        print("2. Pesquisar Usuário")
        print("3. Recarregar Saldo")
        print("4. Registrar Acesso")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            guiche.listar_usuarios()
        elif opcao == "2":
            user_id = input("Digite o ID do usuário para pesquisar: ")
            guiche.pesquisar_usuario(user_id)
        elif opcao == "3":
            user_id = input("Digite o ID do usuário para recarregar o saldo: ")
            try:
                valor = float(input("Digite o valor a ser adicionado ao saldo: R$ "))
                if valor <= 0:
                    print("Valor inválido! O valor precisa ser maior que zero.")
                    continue
                guiche.recarregar_saldo(user_id, valor)
            except ValueError:
                print("Por favor, insira um valor numérico válido.")
        elif opcao == "4":
            user_id = input("Digite o ID do usuário para registrar o acesso: ")
            guiche.verifica_catraca(user_id)
        elif opcao == "5":
            print("Saindo do guichê...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
