import enum
from typing import List
import uuid

from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyBaseOAuthAccountTableUUID,
)
from sqlalchemy import String, JSON, ForeignKey, DDL, event, VARCHAR
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from my_type_notation import added_at, intpk, default_int
from trouble.models import Trouble


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


# модель пользователя для базы данных
class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    @staticmethod
    def default_fullname(context):
        fullname = f'{context.get_current_parameters()["firstname"]} {context.get_current_parameters()["lastname"]}'
        return fullname

    firstname: Mapped[str] = mapped_column(String(length=40), nullable=True)
    lastname: Mapped[str] = mapped_column(String(length=40), nullable=True)
    fullname: Mapped[str] = mapped_column(default=default_fullname)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=1)
    role: Mapped["Role"] = relationship(
        back_populates="users", uselist=False
    )
    email: Mapped[str]
    reported_troubles = relationship('Trouble', back_populates='reporter')
    resolved_troubles = relationship('Trouble', secondary="resolver_trouble", back_populates='resolvers')
    is_email_confirmed: Mapped[bool] = mapped_column(default=False)
    email_confirmation_token = mapped_column(nullable=True, type_=String(50))
    registered_at: Mapped[added_at]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=True)
    pathfile: Mapped[str] = mapped_column(nullable=True)
    search_vector = mapped_column(TSVECTOR)
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )


create_index = DDL(
    "CREATE INDEX search_vector_index ON users USING GIN(search_vector);"
)
event.listen(User.__table__, 'after_create', create_index)


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    permissions: Mapped[dict] = mapped_column(JSON)
    users: Mapped[list["User"]] = relationship(back_populates="role", uselist=True)

