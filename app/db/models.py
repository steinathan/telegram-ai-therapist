import datetime
from sqlalchemy import BigInteger, Column, DateTime, Numeric, func
from sqlmodel import SQLModel, Field
from telegram import User as TelegramUser


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore
    id: int = Field(
        default=None, sa_column=Column(Numeric(), primary_key=True, autoincrement=True)
    )
    telegram_id: int = Field(default=None, sa_column=Column(Numeric()))

    full_name: str

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

    @property
    def real_id(self):
        return int(self.telegram_id)


class Chat(SQLModel, table=True):
    __tablename__ = "chats"  # type: ignore
    id: int = Field(
        default=None, sa_column=Column(Numeric, primary_key=True, autoincrement=True)
    )
    user_id: int = Field(default=None, sa_column=Column(Numeric(), primary_key=True))
    role: str
    text: str
    created_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow,
    )
    updated_at: datetime.datetime | None = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column=Column(DateTime(), onupdate=func.now()),
    )
