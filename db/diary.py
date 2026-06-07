from .base import *

class Note(BaseORM):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    
    created_at: Mapped[date] = mapped_column(default=date.today)
    updated_at: Mapped[date] = mapped_column(default=date.today, onupdate=date.today)
