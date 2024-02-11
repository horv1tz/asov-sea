import os

import fastapi
from fastapi import Depends, UploadFile, Response
from fastapi_cache.decorator import cache
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from auth.base_config import current_user
from auth.models import User, Trouble
from constants import IMAGES_DIR
from database import get_async_session
from trouble.models import CategoryTrouble
#from trouble.models import Trouble
from trouble.schemas import TroubleAdd, TroubleUpdate
from utils import trouble_on_map, main_info_trouble, detailed_info_trouble, create_upload_avatar

router = fastapi.APIRouter(prefix="/troubles", tags=["troubles"])


@router.post("/add_category")
async def add_category(
    name: str,
    session: AsyncSession = Depends(get_async_session)
):
    category = CategoryTrouble(name=name)
    session.add(category)
    await session.commit()
    return {"status": "success"}


@router.delete("/delete_category/{cat_id}")
async def delete_trouble(
    cat_id: int,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
):
    cat = await session.get(CategoryTrouble, cat_id)
    await session.delete(cat)
    await session.commit()
    response.status_code = HTTP_204_NO_CONTENT
    return {"status": "successful delete"}


@router.get("/get_all")
#@cache(expire=10) # можно поставить кэш в секундах, первый запрос будет долгим, а потом все остальные за это время моментальные
async def get_all_troubles(
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        text("SELECT * FROM trouble")
    )
    res = await session.execute(query)
    troubles = res.mappings().all()
    result = {f"trouble{num}": await trouble_on_map(trouble) for num, trouble in enumerate(troubles)}
    return result


@router.get("/get_main_info/{trouble_id}")
async def get_detailed_trouble(
    trouble_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    trouble = (await session.execute(
        select(Trouble).where(Trouble.id == trouble_id).options(
            joinedload(Trouble.category)
        )
    )).unique().scalar_one()
    return await main_info_trouble(trouble)


@router.post("/add_new")
async def add_trouble(
    trouble_data: TroubleAdd,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    # Создание объекта Trouble и назначение user_id
    trouble = Trouble(**trouble_data.model_dump(), reporter_id=user.id)

    # Добавление объекта в сессию и сохранение в базе данных
    session.add(trouble)
    await session.commit()

    return {"status": "success"}


@router.get("/get_detailed_info/{trouble_id}")
async def get_detailed_info(
    trouble_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    trouble = await session.get(Trouble, trouble_id)
    return (await detailed_info_trouble(trouble))


@router.post("/uploadfile/avatar")
async def upload_trouble_image(
    file: UploadFile,
    trouble_id: int
):
    class_ = Trouble
    user_avatar_dir = os.path.join(IMAGES_DIR, "trouble")
    res = await create_upload_avatar(trouble_id, file, class_, user_avatar_dir)
    return res


@router.delete("/delete/{problem_id}")
async def delete_trouble(
    trouble_id: int,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
):
    trouble = await session.get(Trouble, trouble_id)
    await session.delete(trouble)
    await session.commit()
    response.status_code = HTTP_204_NO_CONTENT
    return {"status": "successful delete"}


@router.put("/update/{problem_id}")
async def update_trouble(
    trouble_data: TroubleUpdate,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
):
    trouble_data = {key: value for key, value in trouble_data.model_dump().items() if value is not None}
    trouble = await session.get(Trouble, trouble_data.get("id"))
    await session.execute(
        update(Trouble).where(Trouble.id == trouble_data.get("id"))
        .values(trouble_data)
    )
    await session.merge(trouble)
    await session.commit()
    response.status_code = HTTP_204_NO_CONTENT
    return {"status": "successful update"}

