from fastapi import FastAPI

from app.api.routes.users import UserRoutes
from app.api.routes.transactions import TransactionRoutes
from app.db.database import Database
from app.db.models import Models


class Bandpay:
    def __init__(self, db_url: str):
        self.database = Database(db_url=db_url)
        self.app = FastAPI(title="Bandpay API")
        self._setup_routes()

    def _setup_routes(self):
        self.models = Models(self.database.Base)

        User, Transaction = self.models.define()

        user_routes = UserRoutes(self.database, User)
        transaction_routes = TransactionRoutes(self.database, User, Transaction)

        self.app.include_router(user_routes.router, prefix="/users", tags=["users"])
        self.app.include_router(
            transaction_routes.router, prefix="/transactions", tags=["transactions"]
        )

        self.database.create_tables()

    def get_app(self) -> FastAPI:
        return self.app


# put main def here
bandpay = Bandpay("sqlite:///test.db")
app = bandpay.get_app()
