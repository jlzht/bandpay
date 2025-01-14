from fastapi import FastAPI
from app.api.routes.users import UserRoutes
from app.api.routes.transactions import TransactionRoutes
from app.db.database import Database
from app.db.models import Models



app = FastAPI()

#
class Bandpay:
    def __init__(self, db_url: str):
        """
        Inicializa a classe Bandpay, configurando o banco de dados e as rotas da API.
        """
        # Inicializa o banco de dados
        self.database = Database(db_url=db_url)
        self.app = FastAPI(title="Bandpay API")
        self._setup_routes()

    def _setup_routes(self):
        """
        Configura os modelos e as rotas da aplicação.
        """
        # Define os modelos usando a base de dados
        self.models = Models(self.database.base)
        User, Transaction = self.models.define()

        # Inicializa as rotas com a sessão do banco de dados e os modelos
        user_routes = UserRoutes(self.database, User)
        transaction_routes = TransactionRoutes(self.database, User, Transaction)

        # Inclui as rotas na aplicação
        self.app.include_router(user_routes.router, prefix="/users", tags=["users"])
        self.app.include_router(
            transaction_routes.router, prefix="/transactions", tags=["transactions"]
        )

        # Cria as tabelas no banco de dados
        self.database.create_tables()

    def get_app(self) -> FastAPI:
        """
        Retorna a aplicação FastAPI configurada.
        """
        return self.app


# Configurando o banco de dados e inicializando a aplicação
db_url = "sqlite:///./test.db"
bandpay = Bandpay(db_url=db_url)
app = bandpay.get_app()
