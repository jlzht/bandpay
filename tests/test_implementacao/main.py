from apiClient import ApiClient  
from user import User  
from transaction import Transaction  
from catraca import Catraca  

# Função que exibe o menu de opções no guichê
def menu():
    # Define a URL da API
    api_url = "http://127.0.0.1:8000"
    api_client = ApiClient(api_url)  # Cria uma instância do cliente da API

    while True:
        # Exibe as opções do menu
        print("\nMenu do Guichê:")
        print("1. Listar Usuários")
        print("2. Pesquisar Usuário")
        print("3. Recarregar Saldo")
        print("4. Registrar Acesso")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

    
        if opcao == "1":
            user = User(None, api_client)  # Cria uma instância de User sem ID
            user.listar_usuarios()  # Chama o método para listar os usuários
        
        elif opcao == "2":
            user_id = input("Digite o ID do usuário para pesquisar: ")
            user = User(user_id, api_client)  # Cria uma instância de User com o ID fornecido
            user.pesquisar_usuario(user_id)  # Chama o método para pesquisar o usuário pelo ID
       
        elif opcao == "3":
            user_id = input("Digite o ID do usuário para recarregar o saldo: ")
            user = User(user_id, api_client)  # Cria uma instância de User com o ID fornecido
            try:
                # Solicita o valor a ser adicionado ao saldo
                valor = float(input("Digite o valor a ser adicionado ao saldo: R$ "))
                transaction = Transaction(user_id, valor, api_client)  # Cria uma transação
                transaction.registrar()  # Chama o método para registrar a transação e recarregar o saldo
            except ValueError:
                # Caso o valor fornecido não seja válido, exibe um erro
                print("Erro: Valor inválido para recarga. Retornando ao menu.")
        
        elif opcao == "4":
            user_id = input("Digite o ID do usuário para registrar o acesso: ")
            user = User(user_id, api_client)  # Cria uma instância de User com o ID fornecido
            catraca = Catraca(user, api_client)  # Cria uma instância de Catraca para verificar o acesso
            catraca.verificar_e_decrementar()  # Chama o método para verificar e decrementar o acesso
        
        elif opcao == "5":
            print("Saindo do guichê...")
            break  
        # Caso a opção seja inválida, exibe uma mensagem de erro
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu()
