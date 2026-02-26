import logging
import os
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .config import settings
from .database import engine, SessionLocal
from .models import User, Shop, Employee, Record, Log
from .models.user import UserRole
from .services.auth import get_password_hash
from .routers import auth, users, shops, employees, records, logs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    from .database import Base
    Base.metadata.create_all(bind=engine)

def create_default_superadmin():
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == settings.FIRST_SUPERADMIN_EMAIL).first()
        if not existing:
            admin = User(
                id=str(uuid.uuid4()),
                email=settings.FIRST_SUPERADMIN_EMAIL,
                hashed_password=get_password_hash(settings.FIRST_SUPERADMIN_PASSWORD),
                full_name=settings.FIRST_SUPERADMIN_NAME,
                role=UserRole.super_admin,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            logger.info(f"Default superadmin created: {settings.FIRST_SUPERADMIN_EMAIL} / {settings.FIRST_SUPERADMIN_PASSWORD}")
        else:
            logger.info(f"Superadmin already exists: {settings.FIRST_SUPERADMIN_EMAIL}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    create_default_superadmin()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield

app = FastAPI(
    title="Fix App API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(users.router, prefix=API_PREFIX)
app.include_router(shops.router, prefix=API_PREFIX)
app.include_router(employees.router, prefix=API_PREFIX)
app.include_router(records.router, prefix=API_PREFIX)
app.include_router(logs.router, prefix=API_PREFIX)

uploads_dir = settings.UPLOAD_DIR
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

@app.get("/api/health")
def health():
    return {"status": "ok"}
