import time
import requests
import uvicorn

# Base URLs (ajustar conforme sua API)
BASE_URL = "http://127.0.0.1:8000"  # Verifique se está correto para a sua API
USER_ENDPOINT = f"{BASE_URL}/users"
TRANSACTION_ENDPOINT = f"{BASE_URL}/transactions"

# Variável para contar os testes que passaram
passed_tests = 0
total_tests = 0

# Função para testar a criação de um usuário
def test_create_user():
    global passed_tests, total_tests
    print("Testing user creation...")
    user_data = {
        "id": "20240000",
        "name": "Davi Britto",
        "status": "active"
    }
    
    try:
        response = requests.post(USER_ENDPOINT, json=user_data)
        total_tests += 1
        # Verifique se a resposta foi bem-sucedida
        if response.status_code == 200:
            print("User created successfully:", response.json())
            passed_tests += 1
        else:
            print(f"Failed to create user. Status code: {response.status_code}. Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating user: {e}")
        total_tests += 1

# Função para testar a obtenção de dados de um usuário
def test_get_user():
    global passed_tests, total_tests
    print("Testing get user...")
    user_id = "20240000"
    
    try:
        response = requests.get(f"{USER_ENDPOINT}/{user_id}")
        total_tests += 1
        # Verifique se a resposta foi bem-sucedida
        if response.status_code == 200:
            print("User data retrieved:", response.json())
            passed_tests += 1
        else:
            print(f"Failed to get user. Status code: {response.status_code}. Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error getting user: {e}")
        total_tests += 1

# Função para testar a criação de uma transação em dinheiro
def test_create_money_transaction():
    global passed_tests, total_tests
    print("Testing money transaction creation...")
    transaction_data = {
        "user_id": "20240000",
        "amount": 100.0,
        "opt": "money"
    }

    try:
        response = requests.post(TRANSACTION_ENDPOINT, json=transaction_data)
        total_tests += 1
        # Verifique se a resposta foi bem-sucedida
        if response.status_code == 200:
            print("Money transaction created successfully:", response.json())
            passed_tests += 1
        else:
            print(f"Failed to create transaction. Status code: {response.status_code}. Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating money transaction: {e}")
        total_tests += 1

# Função para testar a criação de uma transação de transferência
def test_create_transfer_transaction():
    global passed_tests, total_tests
    print("Testing transfer transaction creation...")
    transaction_data = {
        "user_id": "20240000",
        "amount": 50.0,
        "opt": "transfers"
    }
    
    try:
        response = requests.post(TRANSACTION_ENDPOINT, json=transaction_data)
        total_tests += 1
        # Verifique se a resposta foi bem-sucedida
        if response.status_code == 200:
            print("Transfer transaction created successfully:", response.json())
            passed_tests += 1
        else:
            print(f"Failed to create transaction. Status code: {response.status_code}. Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating transfer transaction: {e}")
        total_tests += 1

# Função principal que executa os testes
if __name__ == "__main__":
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
    print("\nGetting user changes...")
    test_get_user()

    print("\nAll tests completed.")
    print(f"\n{passed_tests} out of {total_tests} tests passed.")
