from schemas.roles import UserRole

from .base import *

class User(BaseORM):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    role: Mapped[UserRole] = mapped_column(default=UserRole.ADMIN)

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[date] = mapped_column(default=date.today)
    updated_at: Mapped[date] = mapped_column(default=date.today, onupdate=date.today)

    def __repr__(self):
        return (
            f"User("
            f"id={self.id}, "
            f"username='{self.username}', "
            f"email='{self.email}', "
            f"role='{self.role.value}', "
            f"is_active={self.is_active}"
            f")"
        )