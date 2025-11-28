from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


from ..models.project import Project  # noqa: E402, F401
from ..models.task import Task  # noqa: E402, F401
