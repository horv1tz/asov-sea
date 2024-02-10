from typing import Optional

from pydantic import BaseModel


class TroubleAdd(BaseModel):
    name: str
    description: str
    priority: str
    latitude: float
    longitude: float
    category_id: int


class TroubleUpdate(BaseModel):
    id: int
    solved: str
    name: Optional[str]
    description: Optional[str]
    priority: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    category_id: Optional[int]
