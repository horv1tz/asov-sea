import fastapi
from fastapi import Depends
from sqlalchemy import func, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from auth.models import User
from database import get_async_session
from utils import change_layout, find_object

router = fastapi.APIRouter(prefix="/social", tags=["social"])


@router.get("/find-user")
async def find_user(
    initials: str,
):
    result = await find_object(User, User.fullname, initials, 0.3)
    return result
