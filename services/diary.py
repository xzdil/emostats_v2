from db.diary import Note
from schemas.diary import NoteCreate, NoteUpdate
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
    
    def get_notes_by_user(self, user_id: int) -> list[Note]:
        result = self.repo.get_by_user_id(user_id)
        logger.info(f"Retrieved notes for user ID {user_id}: {result}")
        return result

    def delete_note(self, note_id: int) -> None:
        result = self.repo.get_by_id(note_id)
        logger.info(f"Deleting note with ID {note_id}: {result}")
        self.repo.delete(note_id)

    def update_note(self, note_id: int, note_update: NoteUpdate) -> Note | None:
        result = self.repo.update(note_id, **note_update.model_dump())
        logger.info(f"Updated note with ID {note_id}: {result}")
        return result
    
    def classify_note(self, note_id: int, classification: str, classification_confidence: float) -> Note | None:
        result = self.repo.update(note_id, classification=classification, classification_confidence=classification_confidence)
        logger.info(f"Classified note with ID {note_id} as {classification}: {result}")
        return result