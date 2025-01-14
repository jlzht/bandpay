
import requests

class ApiClient:

    def __init__(self, api_url):
        self.api_url = api_url  # Armazena a URL base da API
    
    # Método para realizar uma requisição GET
    def get(self, endpoint):
        # Constrói a URL completa concatenando a URL base com o endpoint
        url = f"{self.api_url}/{endpoint}"
        try:
            # Realiza a requisição GET
            response = requests.get(url)
            # Verifica se a resposta foi bem-sucedida (status 2xx)
            response.raise_for_status()
            return response.json()  # Retorna a resposta em formato JSON
        except requests.exceptions.RequestException as e:
            # Se ocorrer um erro na requisição, exibe a mensagem de erro
            print(f"Erro na requisição GET para {url}: {e}")
            return None  # Retorna None em caso de erro
    
    # Método para realizar uma requisição POST
    def post(self, endpoint, payload):
        # Constrói a URL completa concatenando a URL base com o endpoint
        url = f"{self.api_url}/{endpoint}"
        try:
            # Realiza a requisição POST, enviando o payload como JSON
            response = requests.post(url, json=payload)
            # Verifica se a resposta foi bem-sucedida (status 2xx)
            response.raise_for_status()
            return response.json()  # Retorna a resposta em formato JSON
        except requests.exceptions.RequestException as e:
            # Se ocorrer um erro na requisição, exibe a mensagem de erro
            print(f"Erro na requisição POST para {url}: {e}")
            return None  # Retorna None em caso de erro
    
    # Método para realizar uma requisição PATCH
    def patch(self, endpoint, payload):
        # Constrói a URL completa concatenando a URL base com o endpoint
        url = f"{self.api_url}/{endpoint}"
        try:
            # Realiza a requisição PATCH, enviando o payload como JSON
            response = requests.patch(url, json=payload)
            # Verifica se a resposta foi bem-sucedida (status 2xx)
            response.raise_for_status()
            return response.json()  # Retorna a resposta em formato JSON
        except requests.exceptions.RequestException as e:
            # Se ocorrer um erro na requisição, exibe a mensagem de erro
            print(f"Erro na requisição PATCH para {url}: {e}")
            return None  # Retorna None em caso de erro
    
    # Método para realizar uma requisição PUT
    def put(self, endpoint, payload):
        # Constrói a URL completa concatenando a URL base com o endpoint
        url = f"{self.api_url}/{endpoint}"
        try:
            # Realiza a requisição PUT, enviando o payload como JSON
            response = requests.put(url, json=payload)
            # Verifica se a resposta foi bem-sucedida (status 2xx)
            response.raise_for_status()
            return response.json()  # Retorna a resposta em formato JSON
        except requests.exceptions.RequestException as e:
            # Se ocorrer um erro na requisição, exibe a mensagem de erro
            print(f"Erro na requisição PUT para {url}: {e}")
            if response.status_code == 500:
                # Se o status da resposta for 500 (erro interno do servidor), exibe a resposta completa
                print(f"Resposta do servidor: {response.text}")
            return None  