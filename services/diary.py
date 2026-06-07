from db.diary import Note
from schemas.diary import NoteCreate
from repositories.diary import NoteRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NoteService:
    def __init__(self, repo: NoteRepository ):
        self.repo = repo

    def create_note(self, note_create: NoteCreate) -> Note:
        result = self.repo.create(**note_create.model_dump())
        logger.info(f"Note created with ID: {result.id}")
        return result

    def get_note(self, note_id: int) -> Note | None:
        result = self.repo.get_by_id(note_id)
        logger.info(f"Retrieved note with ID {note_id}: {result}")  
        return result
    
    def delete_note(self, note_id: int) -> None:
        result = self.repo.get_by_id(note_id)
        logger.info(f"Deleting note with ID {note_id}: {result}")