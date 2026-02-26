import os
import time
import uuid
from datetime import date
from pathlib import Path
from fastapi import UploadFile
from ..config import settings

def get_upload_path(shop_id: str, employee_id: str, extension: str) -> str:
    today = date.today().isoformat()
    uid = str(uuid.uuid4())[:8]
    timestamp = int(time.time())
    filename = f"{timestamp}_{uid}.{extension}"
    rel_path = os.path.join(shop_id, today, employee_id, filename)
    return rel_path

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "jpg", "jpeg", "png", "gif", "webp", "heic", "heif",
    "mp4", "mov", "avi", "webm", "mkv", "3gp",
}

async def save_file(file: UploadFile, shop_id: str, employee_id: str) -> tuple[str, int, str]:
    raw_ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else "bin"
    extension = raw_ext if raw_ext in ALLOWED_EXTENSIONS else "bin"
    rel_path = get_upload_path(shop_id, employee_id, extension)
    full_path = os.path.join(settings.UPLOAD_DIR, rel_path)
    ensure_dir(os.path.dirname(full_path))
    
    content = await file.read()
    with open(full_path, "wb") as f:
        f.write(content)
    
    return rel_path, len(content), file.content_type or "application/octet-stream"
