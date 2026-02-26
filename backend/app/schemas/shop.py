from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShopBase(BaseModel):
    name: str
    address: Optional[str] = None

class ShopCreate(ShopBase):
    pass

class ShopUpdate(ShopBase):
    name: Optional[str] = None

class ShopOut(ShopBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
