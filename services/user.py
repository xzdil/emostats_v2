from db.user import User
from schemas.user import UserCreate, UserDB
from repositories.user import UserRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from core.security import verify_password, get_password_hash

class UserService:
    def __init__(self, repo: UserRepository ):
        self.repo = repo

    def create_user(self, user_create: UserCreate) -> User:
        result = self.repo.create(**user_create.model_dump())
        logger.info(f"User created with ID: {result.id}")
        return result
    
    def get_user(self, user_id: int) -> User | None:
        result = self.repo.get_by_id(user_id)
        logger.info(f"Retrieved user with ID {user_id}: {result}")  
        return result

    def get_user_by_username(self, username: str) -> User | None:
        result = self.repo.get_by_username(username)
        if result:
            logger.info(f"Retrieved user with username {username}: {result}")
            return result
        return None

    def delete_user(self, user_id: int) -> None:
        result = self.repo.get_by_id(user_id)
        if result:
            logger.info(f"Deleting user with ID {user_id}: {result.username}")
            self.repo.delete(user_id)
        else:
            logger.info(f"User with ID {user_id} not found for deletion")

    def authenticate_user(self, username: str, password: str) -> UserDB | None:
        """Аутентифицирует пользователя: проверяет, что такой есть и пароль верный"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        logger.info(f"User authenticated successfully: {user.username}")
        return UserDB.model_validate(user)
    
    def register_user(self, user_create: UserCreate) -> UserDB:
        """Регистрирует нового пользователя: хеширует пароль и сохраняет в БД"""
        password = get_password_hash(user_create.password)
        user_data = user_create.model_dump()
        user_data['password'] = password
        user = self.repo.create(**user_data)
        logger.info(f"User registered successfully: {user.username}")
        return UserDB.model_validate(user)