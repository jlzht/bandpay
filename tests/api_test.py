import sys
import os
sys.path.append(os.path.abspath('../app'))  # Adiciona o caminho absoluto para 'app'

from multiprocessing import Process
from app.main import Bandpay
from app.bank import BankAPI
import time
import requests
import uvicorn


# Base URLs (ajustar conforme sua API)
BASE_URL = "http://localhost:8080"  # Replace with your actual base API URL for Bandpay
USER_ENDPOINT = f"{BASE_URL}/users"
TRANSACTION_ENDPOINT = f"{BASE_URL}/transactions"

def start_bank_api():
    bank_api = BankAPI()
    app = bank_api.get_app()
    uvicorn.run(app, host="127.0.0.1", port=8083)

def start_bandpay():
    bandpay = Bandpay("sqlite:///test.db")
    app = bandpay.get_app()
    uvicorn.run(app, host="127.0.0.1", port=8080)

# Função para testar a criação de um usuário
def test_create_user():
    print("Testing user creation...")
    user_data = {
        "id": "20240000",
        "name": "Davi Britto",
        "status": "active"
    }
    response = requests.post(USER_ENDPOINT, json=user_data)
    print("Response:", response.status_code, response.json())

# Função para testar a obtenção de dados de um usuário
def test_get_user():
    print("Testing get user...")
    user_id = "20240000"
    response = requests.get(f"{USER_ENDPOINT}/{user_id}/")
    print("Response:", response.status_code, response.json())

# Função para testar a criação de uma transação em dinheiro
def test_create_money_transaction():
    print("Testing money transaction creation...")
    transaction_data = {
        "user_id": "20240000",
        "amount": 100.0,
        "opt": "money"
    }
    response = requests.post(TRANSACTION_ENDPOINT, json=transaction_data)
    print("Response:", response.status_code, response.json())

# Função para testar a criação de uma transação de transferência
def test_create_transfer_transaction():
    print("Testing transfer transaction creation...")
    transaction_data = {
        "user_id": "20240000",
        "amount": 50.0,
        "opt": "transfers"
    }
    response = requests.post(TRANSACTION_ENDPOINT, json=transaction_data)
    print("Response:", response.status_code, response.json())

# Função principal que inicia os processos para ambos os APIs e executa os testes
if __name__ == "__main__":
    # Inicia os processos para ambos os APIs
    bank_api_process = Process(target=start_bank_api)
    bandpay_process = Process(target=start_bandpay)

    # Inicia os processos
    bank_api_process.start()
    bandpay_process.start()

    # Aguarda alguns segundos para garantir que os serviços tenham iniciado corretamente
    time.sleep(5)

    print("Starting API Tests...\n")
    
    # Executa os testes
    test_create_user()
    print("\n")
    test_get_user()
    print("\n")
    test_create_money_transaction()
    print("\n")
    test_create_transfer_transaction()
    
    # Verifica novamente os dados do usuário após as transações
    print("Getting user changes...")
    test_get_user()
    
    print("\nAll tests completed.")

    # Espera os processos terminarem antes de finalizar
    bank_api_process.join()
    bandpay_process.join()
