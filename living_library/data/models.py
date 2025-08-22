from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey, select, DateTime, update, delete
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Mapped, mapped_column

from living_library.data.database import Base
from living_library.data.static.genre import Genre

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

class Post(Base):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)
    uri: Mapped[str] = mapped_column(nullable=False)

class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=True)
    genre: Mapped[int] = mapped_column(nullable=False)
    state: Mapped[int] = mapped_column(default=0)
    uri: Mapped[str] = mapped_column(nullable=False)

