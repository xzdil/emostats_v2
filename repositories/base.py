from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        db: Session,
        model: Type[ModelType]
    ):
        self.db = db
        self.model = model

    def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def get_by_id(self, obj_id: int) -> ModelType | None:
        return self.db.get(self.model, obj_id)

    def get_all(self) -> list[ModelType]:
        return self.db.query(self.model).all()

    def update(
        self,
        obj_id: int,
        **kwargs
    ) -> ModelType | None:
        obj = self.get_by_id(obj_id)

        if obj is None:
            return None

        for key, value in kwargs.items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return obj

    def delete(self, obj_id: int) -> bool:
        obj = self.get_by_id(obj_id)

        if obj is None:
            return False

        self.db.delete(obj)
        self.db.commit()

        return True