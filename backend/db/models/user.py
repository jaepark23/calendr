from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, DateTime
from sqlalchemy import Integer, Enum
from sqlalchemy.sql import func
from enum import Enum as PyEnum

class Base(DeclarativeBase):
    pass

class AuthType(PyEnum):
    email = "email"
    google = "google"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique = True, nullable=False)
    password = Column(String, nullable=True)
    auth_type = Column(Enum(AuthType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable= False)
    num_docs = Column(Integer, nullable= False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"