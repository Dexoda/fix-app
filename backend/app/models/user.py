import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
import enum

class UserRole(str, enum.Enum):
    super_admin = "super_admin"
    shop_admin = "shop_admin"
    director = "director"

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), nullable=False, default=UserRole.shop_admin)
    shop_id: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    shop = relationship("Shop", back_populates="users", foreign_keys=[shop_id], primaryjoin="User.shop_id == Shop.id")
    logs = relationship("Log", back_populates="user")
    uploaded_records = relationship("Record", back_populates="uploader", foreign_keys="Record.uploaded_by")
    checked_records = relationship("Record", back_populates="checker", foreign_keys="Record.checked_by")
