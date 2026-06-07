from db.diary import Note
from .base import *

class NoteRepository(BaseRepository[Note]):
    def __init__(self, db: Session):
        super().__init__(db, Note)