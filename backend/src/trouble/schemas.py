from pydantic import BaseModel


class TroubleAdd(BaseModel):
    name: str
    description: str
    priority: str
    latitude: float
    longitude: float
    category_id: int
