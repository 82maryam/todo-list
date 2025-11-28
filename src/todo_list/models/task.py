from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, ForeignKey, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)

    status: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="todo"
    )

    deadline: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    closed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )
