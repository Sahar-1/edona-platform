from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None

class ItemResponse(ItemCreate):
    id: int
    status: str

    class Config:
        from_attributes = True