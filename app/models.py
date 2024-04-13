from sqlmodel import SQLModel, Field, create_engine, Session, select
from telegram import User as TelegramUser


class User(SQLModel):
    id: int = Field(default=None, primary_key=True)
    full_name: str
    chat_id: int


engine = create_engine("sqlite:///database.db")

with Session(engine) as session:
    statement = select(User).where(User.name == "Spider-Boy")
    hero = session.exec(statement).first()
    print(hero)
