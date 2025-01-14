import requests

class User:
    def __init__(self, user_id, api_client):
        self.user_id = user_id
        self.api_client = api_client
        self.api_url = api_client.api_url  # Acessando o api_url do api_client
    
    def consultar_saldo(self):
        """
        Consulta o saldo de um usuário específico.
        """
        url = f"{self.api_url}/users/{self.user_id}/balance"  # Corrigindo a URL para usar o api_url
        try:
            response = requests.get(url)
            response.raise_for_status()  # Levanta um erro para status 4xx/5xx
            return response.json().get("balance")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar saldo: {e}")
            return None

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
