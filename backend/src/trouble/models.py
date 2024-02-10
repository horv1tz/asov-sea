import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from my_type_notation import intpk, added_at


class TroubleState(Enum):
    in_process = "В процессе"
    solved = "Решено"
    not_solved = "Не решено"


class Trouble(Base):
    __tablename__ = "trouble"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(String(400))
    date_created: Mapped[added_at]
    priority: Mapped[str]
    solved: Mapped[str] = mapped_column(default="Не решено")
    date_solved: Mapped[datetime.datetime] = mapped_column(nullable=True)
    latitude: Mapped[float]
    longitude: Mapped[float]
    pathfile: Mapped[str] = mapped_column(nullable=True)
    reporter_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    reporter = relationship('User', back_populates='reported_troubles', foreign_keys=[reporter_id])
    resolvers = relationship('User', secondary="resolver_trouble", back_populates='resolved_troubles')
    category_id: Mapped[int] = mapped_column(ForeignKey("category_trouble.id"))
    category = relationship(
        "CategoryTrouble",
        back_populates="troubles", uselist=False
    )


class ResolverProblem(Base):
    __tablename__ = "resolver_trouble"

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), primary_key=True)
    trouble_id: Mapped[int] = mapped_column(ForeignKey('trouble.id'), primary_key=True)


class CategoryTrouble(Base):
    __tablename__ = "category_trouble"

    id: Mapped[intpk]
    name: Mapped[str]
    troubles = relationship(
        "Trouble",
        back_populates="category", uselist=True
    )
