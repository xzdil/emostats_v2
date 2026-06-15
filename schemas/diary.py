from typing import Any
from enum import Enum

from pydantic import field_validator
from .base import *

class Classification(int, Enum):
    HAPPY = 1
    SAD = 2
    ANGRY = 3

class NoteClassification(BaseValidateModel):
    classification: Optional[Classification] = None
    classification_confidence: Optional[float] = None

    @field_validator('classification_confidence')
    def validate_classification_confidence(cls, value):
        if value is not None and not 0 <= value <= 1:
            raise ValueError("Classification confidence must be a float between 0 and 1")
        return value

class NoteBase(BaseValidateModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteCreate(NoteBase):
    user_id: int

class NoteDB(NoteCreate):
    id: int

class NoteUpdate(BaseValidateModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(BaseValidateModel):
    id: int
    user_id: int
    title: Optional[Any] = None
    content: Optional[Any] = None
    classification: Optional[Any] = None
    classification_confidence: Optional[Any] = None
    updated_at: Optional[Any] = None
    created_at: Optional[Any] = None