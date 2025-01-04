from fastapi import APIRouter, HTTPException, Depends, Path, Body
from sqlalchemy.orm import Session
from typing import Any

from app.db.schemas import UserCreate


class UserRoutes:
    def __init__(self, database, User):
        self.User = User
        self.database = database
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        # Retrieve all data for a specific user
        @self.router.get("/{user_id}/")
        def get_user(user_id: int, db: Session = Depends(self.database.get_session)):
            user = db.query(self.User).filter(self.User.id == user_id).first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return {
                "id": user.id,
                "name": user.name,
                "balance": user.balance,
                "status": user.status,
            }

        # Create a new user
        @self.router.post("/")
        def create_user(
            user: UserCreate, db: Session = Depends(self.database.get_session)
        ):
            existing_user = db.query(self.User).filter(self.User.id == user.id).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")

            new_user = self.User(
                id=user.id, name=user.name, balance=0.0, status=user.status
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "id": new_user.id,
                "name": new_user.name,
                "balance": new_user.balance,
                "status": new_user.status,
            }

        # Delete a specific user
        @self.router.delete("/{user_id}/")
        def delete_user(user_id: int, db: Session = Depends(self.database.get_session)):
            user = db.query(self.User).filter(self.User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            db.delete(user)
            db.commit()
            return {"detail": f"User {user_id} deleted successfully"}

        # Retrieve a specific field of a user
        @self.router.get("/{user_id}/{field}/")
        def get_field(
            user_id: int,
            field: str = Path(..., description="Field to retrieve"),
            db: Session = Depends(self.database.get_session),
        ):
            user = db.query(self.User).filter(self.User.id == user_id).first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if not hasattr(user, field):
                raise HTTPException(
                    status_code=400, detail=f"Field '{field}' does not exist"
                )

            return {"id": user.id, field: getattr(user, field)}

        # Update a specific field of a user
        @self.router.put("/{user_id}/{field}/")
        def set_field(
            user_id: int,
            field: str = Path(..., description="Field to be updated"),
            value: Any = Body(..., description="New value for the field"),
            db: Session = Depends(self.database.get_session),
        ):
            user = db.query(self.User).filter(self.User.id == user_id).first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if not hasattr(user, field):
                raise HTTPException(
                    status_code=400, detail=f"Field '{field}' does not exist"
                )

            setattr(user, field, value)
            db.commit()
            db.refresh(user)

            return {"id": user.id, field: getattr(user, field)}
