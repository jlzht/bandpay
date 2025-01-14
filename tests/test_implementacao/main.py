from apiClient import ApiClient
from user import User
from transaction import Transaction
from catraca import Catraca

def menu():
    api_url = "http://127.0.0.1:8000"
    api_client = ApiClient(api_url)

    while True:
        print("\nMenu do Guichê:")
        print("1. Listar Usuários")
        print("2. Pesquisar Usuário")
        print("3. Recarregar Saldo")
        print("4. Registrar Acesso")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            user = User(None, api_client) 
            user.listar_usuarios()  # Chama o método para listar os usuários
        elif opcao == "2":
            user_id = input("Digite o ID do usuário para pesquisar: ")
            user = User(user_id, api_client)
            user.pesquisar_usuario(user_id)  # Chama o método para pesquisar o usuário pelo ID
        elif opcao == "3":
            user_id = input("Digite o ID do usuário para recarregar o saldo: ")
            user = User(user_id, api_client)
            try:
                valor = float(input("Digite o valor a ser adicionado ao saldo: R$ "))
                transaction = Transaction(user_id, valor, api_client)
                transaction.registrar()  # Chama o método para registrar a transação e recarregar o saldo
            except ValueError:
                print("Erro: Valor inválido para recarga. Retornando ao menu.")
        elif opcao == "4":
            user_id = input("Digite o ID do usuário para registrar o acesso: ")
            user = User(user_id, api_client)
            catraca = Catraca(user, api_client)
            catraca.verificar_e_decrementar()
        elif opcao == "5":
            print("Saindo do guichê...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
