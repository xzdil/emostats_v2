from db.user import User
from .base import *

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(self.model).filter(self.model.username == username).first()