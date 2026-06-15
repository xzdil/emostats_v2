from fastapi import FastAPI, Depends, HTTPException
from pydantic import ValidationError
from core.database import get_db
from core.auth import get_api_token, get_current_user
from repositories.diary import NoteRepository
from services.diary import NoteService
from schemas.diary import NoteBase, NoteClassification, NoteCreate, NoteUpdate, NoteResponse
from sqlalchemy.orm import Session

from services.classification import ClassificationService

def register_diary_route(app: FastAPI):
    @app.get("/note/{id}/get", response_model=NoteCreate,
             summary="Получить заметку по айди",tags=["Заметки"])
    def get_note(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
        if not current_user.role == "admin":
            raise HTTPException(status_code=403, detail="Not authorized to access this note")
        note = NoteService(repo=NoteRepository(db)).get_note(id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    
    @app.get("/note/all/{user_id}/get", response_model=list[NoteResponse],
             summary="Получить заметки по айди пользователя",tags=["Заметки"])
    def get_notes(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
        if current_user.id != user_id or not current_user.role == "admin":
            raise HTTPException(status_code=403, detail="Not authorized to access these notes")
        notes = NoteService(repo=NoteRepository(db)).get_notes_by_user(user_id)
        if len(notes) == 0:
            raise HTTPException(status_code=404, detail="Notes not found")
        return notes

    @app.post("/note/create", response_model=NoteResponse,
              summary="Создать заметку",tags=["Заметки"])
    def create_note(note_create: NoteBase, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
        note_create = NoteCreate(**note_create.model_dump(), user_id=current_user.id)
        note_create.user_id = current_user.id 
        try:
            note = NoteService(repo=NoteRepository(db)).create_note(note_create)
            classification_result = ClassificationService().create_classification(note.content)
            note = NoteService(repo=NoteRepository(db)).classify_note(note.id, **NoteClassification(**classification_result).model_dump())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail="Validation error during classification: " + str(e))
        return note
        

    @app.put("/note/{id}/update", response_model=NoteResponse,
             summary="Обновить заметку по айди",tags=["Заметки"])
    def update_note(id: int, note_update: NoteUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
        note_service = NoteService(repo=NoteRepository(db))
        note = note_service.get_note(id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        if not current_user.role == "admin" or current_user.id != note.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this note")
        updated_note = note_service.update_note(id, note_update)
        return updated_note

    @app.delete("/note/{id}/delete", response_model=None,
                summary="Удалить заметку по айди",tags=["Заметки"])
    def delete_note(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
        note_service = NoteService(repo=NoteRepository(db))
        note = note_service.get_note(id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        if not current_user.role == "admin" or current_user.id != note.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete notes")
        note_service.delete_note(id)
        return {"status": "success", "message": f"Note {id} deleted successfully"}
    
    @app.post("/note/{id}/classify", response_model=NoteResponse,
              summary="Классифицировать заметку по айди",tags=["Заметки"])
    def classify_note(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
        note_service = NoteService(repo=NoteRepository(db))
        note = note_service.get_note(id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        if not current_user.role == "admin" or current_user.id != note.user_id:
            raise HTTPException(status_code=403, detail="Not authorized to classify this note")
        classification_result = ClassificationService().create_classification(note.content)
        try:
            classified_note = note_service.classify_note(id, **NoteClassification(**classification_result).model_dump())
        except ValidationError as e:
            raise HTTPException(status_code=400, detail="Validation error during classification: " + str(e))
        return classified_note