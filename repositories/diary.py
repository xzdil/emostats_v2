from db.diary import Note
from .base import *

class NoteRepository(BaseRepository[Note]):
    def __init__(self, db: Session):
        super().__init__(db, Note) 

    def get_by_user_id(self, user_id: int) -> list[Note]:
        return self.db.query(self.model).filter(self.model.user_id == user_id).all()
        
    