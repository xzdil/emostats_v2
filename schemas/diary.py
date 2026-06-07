from .base import *

class NoteCreate(BaseValidateModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteDB(NoteCreate):
    id: int
