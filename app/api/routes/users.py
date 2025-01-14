from fastapi import HTTPException, Depends, Path, Body
from sqlalchemy.orm import Session
from typing import Any, List
from app.db.schemas import UserCreate
from app.api.routes.routes import Routes

# Classe que gerencia as rotas relacionadas ao modelo de usuário
class UserRoutes(Routes):
    def __init__(self, database, User):
        # Inicializa a classe com o banco de dados e o modelo de usuário
        self.User = User
        super().__init__(database)

    # Método privado para registrar as rotas de usuário
    def _register_routes(self):
        # Rota para buscar todos os usuários
        @self.router.get("/")
        def get_all_users(db: Session = Depends(self.database.get_session)) -> List[dict]:
            """
            Retorna todos os usuários cadastrados.
            """
            # Consulta todos os usuários no banco de dados
            users = db.query(self.User).all()
            if not users:  # Caso não existam usuários, retorna uma lista vazia
                return []
            
            # Retorna os usuários formatados como uma lista de dicionários
            return [
                {"id": user.id, "name": user.name, "balance": user.balance, "status": user.status}
                for user in users
            ]
          

        # Rota para buscar um usuário específico pelo ID
        @self.router.get("/{user_id}/")
        def get_user(user_id: str, db: Session = Depends(self.database.get_session)):
            # Busca o usuário pelo ID
            user = db.query(self.User).filter(self.User.id == user_id).first()

            if not user:  # Caso o usuário não seja encontrado, retorna um erro 404
                raise HTTPException(status_code=404, detail="User not found")

            # Retorna os detalhes do usuário
            return {
                "id": user.id,
                "name": user.name,
                "balance": user.balance,
                "status": user.status,
            }

        # Rota para criar um novo usuário
        @self.router.post("/")
        def create_user(
            user: UserCreate, db: Session = Depends(self.database.get_session)
        ):
            # Verifica se o usuário já existe no banco de dados
            existing_user = db.query(self.User).filter(self.User.id == user.id).first()
            if existing_user:  # Retorna um erro 400 caso o usuário já exista
                raise HTTPException(status_code=400, detail="User already exists")

            # Cria um novo usuário com saldo inicial de 0
            new_user = self.User(
                id=user.id, name=user.name, balance=0.0, status=user.status
            )
            # Adiciona o novo usuário ao banco de dados
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            # Retorna os detalhes do usuário criado
            return {
                "id": new_user.id,
                "name": new_user.name,
                "status": new_user.status,
            }

        # Rota para deletar um usuário pelo ID
        @self.router.delete("/{user_id}/")
        def delete_user(user_id: str, db: Session = Depends(self.database.get_session)):
            # Busca o usuário pelo ID
            user = db.query(self.User).filter(self.User.id == user_id).first()
            if not user:  # Caso o usuário não seja encontrado, retorna um erro 404
                raise HTTPException(status_code=404, detail="User not found")
            # Remove o usuário do banco de dados
            db.delete(user)
            db.commit()
            # Retorna uma mensagem de sucesso
            return {"detail": f"User {user_id} deleted successfully"}

        # Rota para obter um campo específico de um usuário
        @self.router.get("/{user_id}/{field}/")
        def get_field(
            user_id: str,
            field: str = Path(..., description="Field to retrieve"),
            db: Session = Depends(self.database.get_session),
        ):
            # Busca o usuário pelo ID
            user = db.query(self.User).filter(self.User.id == user_id).first()

            if not user:  # Caso o usuário não seja encontrado, retorna um erro 404
                raise HTTPException(status_code=404, detail="User not found")
            if not hasattr(user, field):  # Verifica se o campo existe no modelo
                raise HTTPException(
                    status_code=400, detail=f"Field '{field}' does not exist"
                )

            # Retorna o valor do campo solicitado
            return {"id": user.id, field: getattr(user, field)}

        # Rota para atualizar um campo específico de um usuário
        @self.router.put("/{user_id}/{field}/")
        def set_field(
            user_id: str,
            field: str = Path(..., description="Field to be updated"),
            value: Any = Body(..., description="New value for the field"),
            db: Session = Depends(self.database.get_session),
        ):
            # Busca o usuário pelo ID
            user = db.query(self.User).filter(self.User.id == user_id).first()

            if not user:  # Caso o usuário não seja encontrado, retorna um erro 404
                raise HTTPException(status_code=404, detail="User not found")
            if not hasattr(user, field):  # Verifica se o campo existe no modelo
                raise HTTPException(
                    status_code=400, detail=f"Field '{field}' does not exist"
                )

            # Atualiza o valor do campo
            setattr(user, field, value)
            db.commit()
            db.refresh(user)

            # Retorna o valor atualizado
            return {"id": user.id, field: getattr(user, field)}
        
        # Rota para atualizar o saldo de um usuário
        @self.router.patch("/{user_id}/update_balance")
        def update_balance(
            user_id: str,
            balance: float = Body(..., description="Novo saldo para o usuário"),
            db: Session = Depends(self.database.get_session),
        ):
            # Consulta o usuário pelo ID
            user = db.query(self.User).filter(self.User.id == user_id).first()
            if not user:  # Caso o usuário não seja encontrado, retorna um erro 404
                raise HTTPException(status_code=404, detail="User not found")
            
            # Atualiza o saldo
            user.balance = balance
            db.commit()
            db.refresh(user)

            # Retorna os detalhes do usuário atualizado
            return {
                "id": user.id,
                "name": user.name,
                "balance": user.balance,
                "status": user.status,
            }
