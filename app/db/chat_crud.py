from typing import Any, List, Optional
from sqlmodel import SQLModel, create_engine, Session, select

from app.db.models import Chat


class ChatCRUD:
    def __init__(self, engine):
        self.engine = engine

    def create(self, model: Chat) -> Chat:
        with Session(self.engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model

    def get(self, model_id: int) -> Chat | None:
        with Session(self.engine) as session:
            return session.get(Chat, model_id)

    def update(self, model_id: int, name: str, description: str) -> Chat | None:
        with Session(self.engine) as session:
            model = session.get(Chat, model_id)
            if model:
                model.name = name
                model.description = description
                session.commit()
                session.refresh(model)
                return model

    def delete(self, model_id: int) -> Optional[Chat]:
        with Session(self.engine) as session:
            model = session.get(Chat, model_id)
            if model:
                session.delete(model)
                session.commit()
                return model

    def get_all(self, where=None) -> List[Chat]:
        with Session(self.engine) as session:
            statement = select(Chat)
            if where is not None:
                statement = statement.where(where)
            return session.exec(statement).all()  # type: ignore
