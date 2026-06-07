from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.auth import get_api_token, require_admin
from core.security import create_access_token
from repositories.user import UserRepository
from schemas.user import UserCreate
from services.user import UserService
from schemas.message import Message


def register_users_route(app: FastAPI):
    @app.get("/user/{id}/get", response_model=UserCreate, dependencies=[Depends(get_api_token)],summary="Получить пользователя по айди",tags=["Пользователи"])
    def get_user(id: int, db: Session = Depends(get_db)):
        user = UserService(repo=UserRepository(db)).get_user(id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    @app.post("/user/register", response_model=Message,summary="Создать пользователя",tags=["Пользователи"])
    def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
        user_exists = UserService(repo=UserRepository(db)).get_user_by_username(user_create.username)
        if user_exists:
            raise HTTPException(status_code=400, detail="Username already exists")
        user = UserService(repo=UserRepository(db)).register_user(user_create)
        return Message(status="success", message=f"User {user.username} created successfully")
    
    @app.post("/user/login",tags=["Пользователи"])
    def login_user(username: str, password: str, db: Session = Depends(get_db)):
        service = UserService(UserRepository(db))

        user_exists = service.get_user_by_username(username)
        if not user_exists:
            raise HTTPException(401, "User not found")

        user = service.authenticate_user(username, password)
        if not user:
            raise HTTPException(401, "Invalid credentials")

        token = create_access_token({
            "sub": str(user.id),
            "role": user.role
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    @app.delete("/user/{id}/delete", response_model=Message,dependencies=[Depends(require_admin)],summary="Удалить пользователя по айди",tags=["Пользователи"])
    def delete_user(id: int, db: Session = Depends(get_db)):
        user_service = UserService(repo=UserRepository(db))
        user = user_service.get_user(id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user_service.delete_user(id)
        return Message(status="success", message=f"User {user.username} deleted successfully")