import os
from uuid import UUID

import fastapi
from fastapi import Depends, UploadFile, Request, Response
from fastapi.responses import FileResponse
from sqlalchemy import insert, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from auth.base_config import current_user
from auth.models import User, Role
from auth.schemas import RoleSchema
from constants import IMAGES_DIR
from database import get_async_session
from utils import create_upload_avatar, trouble_to_dict

router = fastapi.APIRouter(prefix="/profile", tags=["user-profile"])


@router.post("/uploadfile/user/avatar")
async def upload_user_avatar(
    file: UploadFile,
    user: User = Depends(current_user)
):
    class_ = User
    user_avatar_dir = os.path.join(IMAGES_DIR, "user")
    res = await create_upload_avatar(user.id, file, class_, user_avatar_dir)
    return res


@router.get("/image/{user_id}")
async def get_image(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    user = await session.get(User, user_id)
    return FileResponse(user.pathfile)


@router.post("/add-role")
async def add_role(
    role: RoleSchema,
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user)
):
    stmt = insert(Role).values(**role.model_dump())
    await session.execute(stmt)
    await session.commit()
    response.status_code = HTTP_201_CREATED


@router.get("/info_profile/{user_id}")
async def get_user_profile_info(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    user_with_troubles = await session.execute(
        select(User).options(selectinload(User.resolved_troubles)).options(selectinload(User.role))
        .filter(User.id == user_id)
    )
    user_with_troubles = user_with_troubles.scalars().first()

    res = {}
    if user_with_troubles is not None:
        troubles = user_with_troubles.resolved_troubles[-3:]
        res["resolved_troubles"] = {
            f"trouble{num}": await trouble_to_dict(trouble) for num, trouble in enumerate(troubles)
        }
    else:
        res["troubles"] = "no resolved problems"

    res["user_info"] = {
        "fullname": user_with_troubles.fullname,
        "id": user_with_troubles.id,
        "role": user_with_troubles.role.name
    }
    return res


@router.get("/all-user-troubles/{user_id}")
async def get_user_troubles(
    user_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    user_with_troubles: User = ((await session.execute(
        select(User).options(joinedload(User.resolved_troubles))
        .filter(User.id == user_id)))
        .unique().first())[0]
    result = {
        f"trouble{num}": await trouble_to_dict(trouble)
        for num, trouble in enumerate(user_with_troubles.resolved_troubles)
    }
    return result
