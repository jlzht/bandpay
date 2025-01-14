import requests

class ApiClient:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def get(self, endpoint):
        url = f"{self.api_url}/{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição GET para {url}: {e}")
            return None
    
    def post(self, endpoint, payload):
        url = f"{self.api_url}/{endpoint}"
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição POST para {url}: {e}")
            return None

    def patch(self, endpoint, payload):
        """
        Método PATCH modificado para aceitar o parâmetro json e enviar o payload como JSON.
        """
        url = f"{self.api_url}/{endpoint}"
        try:
            response = requests.patch(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição PATCH para {url}: {e}")
            return None

    def put(self, endpoint, payload):
        url = f"{self.api_url}/{endpoint}"
        try:
            response = requests.put(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição PUT para {url}: {e}")
            if response.status_code == 500:
                print(f"Resposta do servidor: {response.text}")
            return None
