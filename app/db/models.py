import datetime
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field
from telegram import User as TelegramUser


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore
    id: int = Field(default=None, primary_key=True)
    full_name: str
    telegram_id: int

    is_premium: bool = Field(default=False)

    created_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow,
    )
    updated_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column=Column(DateTime(), onupdate=func.now()),
    )
    last_seen_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow,
    )


class Chat(SQLModel, table=True):
    __tablename__ = "chats"  # type: ignore
    id: int = Field(default=None, primary_key=True)
    user_id: int
    role: str
    text: str
    created_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow,
    )
    updated_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column=Column(DateTime(), onupdate=func.now()),
    )
