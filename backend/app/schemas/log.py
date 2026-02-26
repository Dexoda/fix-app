from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

class LogOut(BaseModel):
    id: str
    user_id: str
    action: str
    metadata: Optional[Any] = None
    created_at: datetime
    user_name: Optional[str] = None

    class Config:
        from_attributes = True
