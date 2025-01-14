class Catraca:
    def __init__(self, user, api_client):
        self.user = user
        self.api_client = api_client
    
    def verificar_e_decrementar(self):
        """
        Verifica se o saldo do usuário é suficiente para registrar um acesso
        e decrementa o valor do saldo.
        """
        saldo_atual = self.user.consultar_saldo()
        
        if saldo_atual is None:
            print("Erro: Não foi possível identificar o saldo do usuário.")
            return

        if saldo_atual > 0:
            # Defina o valor a ser decrementado
            valor_decremento = 5.0

            if saldo_atual >= valor_decremento:
                # Decrementa o saldo    
                novo_saldo = saldo_atual - valor_decremento
                

                # Atualiza o saldo na API
                payload = novo_saldo
        
                response = self.api_client.put(f"users/{self.user.user_id}/balance", payload)

                if response:
                    print(f"Acesso registrado. Novo saldo: R$ {novo_saldo}")
                else:
                    print("Erro ao atualizar saldo do usuário.")
            else:
                print("Erro: Saldo insuficiente para registrar o acesso.")
        else:
            print("Erro: Saldo do usuário é insuficiente.")
