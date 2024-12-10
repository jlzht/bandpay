from fastapi import FastAPI

from app.api.routes.users import UserRoutes
from app.api.routes.transactions import TransactionRoutes

from app.db.database import Database

db_url = "sqlite:///./test.db"
database = Database(db_url=db_url)

database.create_tables()

def create_app() -> FastAPI:
    app = FastAPI(title="Bandpay API")

    user_routes = UserRoutes(database.get_session)
    transaction_routes = TransactionRoutes(database.get_session)

    app.include_router(user_routes.router, prefix="/users", tags=["users"])
    app.include_router(transaction_routes.router, prefix="/transactions", tags=["transactions"])

    return app

app = create_app()
