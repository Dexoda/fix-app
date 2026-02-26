import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
import enum

class RecordType(str, enum.Enum):
    photo = "photo"
    video = "video"
    no_bag = "no_bag"

class Record(Base):
    __tablename__ = "records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type: Mapped[RecordType] = mapped_column(SAEnum(RecordType), nullable=False)
    file_path: Mapped[str | None] = mapped_column(String, nullable=True)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String, nullable=True)
    thumbnail_path: Mapped[str | None] = mapped_column(String, nullable=True)
    shop_id: Mapped[str] = mapped_column(String, ForeignKey("shops.id"), nullable=False)
    employee_id: Mapped[str] = mapped_column(String, ForeignKey("employees.id"), nullable=False)
    uploaded_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    checked_by: Mapped[str | None] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    shop = relationship("Shop", back_populates="records")
    employee = relationship("Employee", back_populates="records")
    uploader = relationship("User", back_populates="uploaded_records", foreign_keys=[uploaded_by])
    checker = relationship("User", back_populates="checked_records", foreign_keys=[checked_by])
