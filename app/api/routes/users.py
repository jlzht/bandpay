from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.models import User
from app.db.schemas import UserCreate

class UserRoutes:
    def __init__(self, database_cb):
        self.database_cb = database_cb
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        @self.router.post("/")
        def create_user(user: UserCreate, db: Session = Depends(self.database_cb)):
            existing_user = db.query(User).filter(User.id == user.id).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")

            new_user = User(id=user.id, name=user.name, balance=0.0, status=user.status)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "id": new_user.id,
                "name": new_user.name,
                "balance": new_user.balance,
                "status": new_user.status,
            }

        @self.router.get("/{user_id}/balance/")
        def get_balance(user_id: int, db: Session = Depends(self.database_cb)):
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {"id": user.id, "balance": user.balance}
