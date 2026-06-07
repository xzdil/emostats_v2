from fastapi import FastAPI, Depends, HTTPException
from core.database import get_db
from core.auth import get_api_token
from repositories.diary import NoteRepository
from services.diary import NoteService
from schemas.diary import NoteCreate
from sqlalchemy.orm import Session

def register_diary_route(app: FastAPI):
    @app.get("/note/{id}/get", response_model=NoteCreate, dependencies=[Depends(get_api_token)],summary="Получить пользователя по айди",tags=["Заметки"])
    def get_user(id: int, db: Session = Depends(get_db)):
        note = NoteService(repo=NoteRepository(db)).get_note(id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return note

    @app.post("/note/create", response_model=NoteCreate,dependencies=[Depends(get_api_token)],summary="Создать пользователя",tags=["Заметки"])
    def create_user(user_create: NoteCreate, db: Session = Depends(get_db)):
        note = NoteService(repo=NoteRepository(db)).create_note(user_create)
        return note