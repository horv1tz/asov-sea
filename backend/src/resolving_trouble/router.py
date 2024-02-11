import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from trouble.models import Trouble

router = fastapi.APIRouter(prefix="/resolving-trouble", tags=["resolving-trouble"])


@router.put("/join-in-resolvers/{trouble_id}")
async def join_in_resolvers(
    trouble_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):

    trouble_query = select(Trouble).where(Trouble.id == trouble_id).options(selectinload(Trouble.resolvers))
    result = await session.execute(trouble_query)
    trouble = result.scalars().first()

    if trouble is None:
        raise HTTPException(status_code=404, detail="Trouble not found")

    if user in trouble.resolvers:
        raise HTTPException(status_code=400, detail="User already a resolver")

    trouble.resolvers.append(user)
    session.add(trouble)
    await session.commit()

    return {"message": "User added to resolvers successfully"}


@router.delete("/left-out-resolvers/{trouble_id}")
async def left_out_resolvers(
    trouble_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):

    trouble_query = select(Trouble).where(Trouble.id == trouble_id).options(selectinload(Trouble.resolvers))
    result = await session.execute(trouble_query)
    trouble = result.scalars().first()

    if trouble is None:
        raise HTTPException(status_code=404, detail="Trouble not found")

    if user not in trouble.resolvers:
        raise HTTPException(status_code=400, detail="User already not a resolver")

    trouble.resolvers.remove(user)
    session.add(trouble)
    await session.commit()

    return {"message": "User removed out resolvers successfully"}
