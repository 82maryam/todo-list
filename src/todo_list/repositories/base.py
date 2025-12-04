from abc import ABC
from sqlalchemy.orm import Session


class SqlAlchemyRepository(ABC):

    def __init__(self, session: Session) -> None:
        self._session = session
