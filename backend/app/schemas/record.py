from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.record import RecordType

class RecordNoBag(BaseModel):
    employee_id: str
    shop_id: str

class RecordOut(BaseModel):
    id: str
    type: RecordType
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    duration: Optional[int] = None
    mime_type: Optional[str] = None
    thumbnail_path: Optional[str] = None
    shop_id: str
    employee_id: str
    uploaded_by: str
    checked_by: Optional[str] = None
    checked_at: Optional[datetime] = None
    created_at: datetime
    employee_name: Optional[str] = None
    uploader_name: Optional[str] = None

    class Config:
        from_attributes = True
