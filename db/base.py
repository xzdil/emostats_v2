from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import date 

class BaseORM(DeclarativeBase):
    __schema__: str = 'public'
    