import fastapi
from fastapi import Depends, Response, UploadFile, Request
from fastapi_users.password import PasswordHelper, PasswordHelperProtocol
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from auth.schemas import UserGoogleRegistration
from database import get_async_session

router = fastapi.APIRouter(prefix="/custom", tags=["custom-auth"])


@router.post("/final_auth_google")
async def set_final_auth_google(
    data: UserGoogleRegistration,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    data = {key: value for key, value in data.model_dump().items() if value is not None}
    pwd = PasswordHelper()
    data["hashed_password"] = pwd.hash(data.get("password"))
    data.pop("password")
    await session.execute(update(User).where(User.id == user.id).values(data))
    await session.merge(user)
    await session.commit()
    return {
        "nickname": user.nickname,
        "password": pwd.hash("string")
    }
