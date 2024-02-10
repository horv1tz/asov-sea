import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr
from typing_extensions import Any, Dict

class UserRead(schemas.BaseUser[uuid.UUID]):

    firstname: str
    lastname: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    pathfile: Optional[str] = None

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    # схема pydantic для взаимодействия с регистрацией
    firstname: str
    lastname: str
    role_id: int
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    pathfile: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserGoogleRegistration(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    password: Optional[str] = None


class RoleSchema(BaseModel):
    name: str
    permissions: Dict[str, Any]


class TeamSchema(BaseModel):
    name: str
    pathfile: str
