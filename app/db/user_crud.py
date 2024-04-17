from typing import List, Optional
from sqlmodel import SQLModel, create_engine, Session, select

from app.db.models import User


class UserCRUD:
    def __init__(self, engine):
        self.engine = engine

    def create(self, model: User) -> User:
        with Session(self.engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)
            return model

    def get(self, model_id: int) -> User | None:
        with Session(self.engine) as session:
            return session.get(User, model_id)

    def update(self, model_id: int, name: str, description: str) -> User | None:
        with Session(self.engine) as session:
            model = session.get(User, model_id)
            if model:
                model.name = name
                model.description = description
                session.commit()
                session.refresh(model)
                return model

    def delete(self, model_id: int) -> Optional[User]:
        with Session(self.engine) as session:
            model = session.get(User, model_id)
            if model:
                session.delete(model)
                session.commit()
                return model

    def get_all(self) -> List[User]:
        with Session(self.engine) as session:
            return session.exec(select(User)).all()  # type: ignore
