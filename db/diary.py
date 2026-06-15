from .base import *

class Note(BaseORM):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    title: Mapped[str] = mapped_column()    
    content: Mapped[str] = mapped_column()
    classification: Mapped[int] = mapped_column(default=0)
    classification_confidence: Mapped[float] = mapped_column(default=0.0)
    
    created_at: Mapped[date] = mapped_column(default=date.today)
    updated_at: Mapped[date] = mapped_column(default=date.today, onupdate=date.today)

    def __repr__(self):
        return (
            f"Note("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"classification='{self.classification}', "
            f"classification_confidence={self.classification_confidence}"
        )  