from app.logging import logger
from sqlmodel import SQLModel, create_engine, Session, select

from app.db.models import *  # noqa: F403


from app.db.chat_crud import ChatCRUD
from app.db.user_crud import UserCRUD

engine = create_engine("sqlite:///database.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    logger.info("Database and tables created")


create_db_and_tables()


# just exporting for convience
user_crud = UserCRUD(engine=engine)
chat_crud = ChatCRUD(engine=engine)
