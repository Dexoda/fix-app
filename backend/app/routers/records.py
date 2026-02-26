from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from ..database import get_db
from ..models.user import User, UserRole
from ..models.record import Record, RecordType
from ..models.log import Log
from ..schemas.record import RecordNoBag, RecordOut
from ..services.file_storage import save_file
from ..dependencies.auth import get_current_user
from ..dependencies.permissions import require_director_or_above
from ..config import settings
import uuid

router = APIRouter(prefix="/records", tags=["records"])

def make_log(db: Session, user_id: str, action: str, meta: dict):
    log = Log(id=str(uuid.uuid4()), user_id=user_id, action=action, metadata=meta)
    db.add(log)

@router.post("/upload", response_model=RecordOut)
async def upload_record(
    employee_id: str = Form(...),
    shop_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content_type = file.content_type or ""
    content = await file.read()
    if content_type.startswith("video/"):
        rec_type = RecordType.video
        if len(content) > settings.MAX_VIDEO_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"Video exceeds {settings.MAX_VIDEO_SIZE_MB}MB limit")
    else:
        rec_type = RecordType.photo

    extension = (file.filename or "file").rsplit(".", 1)[-1].lower() if "." in (file.filename or "") else "bin"
    from ..services.file_storage import get_upload_path, ensure_dir
    rel_path = get_upload_path(shop_id, employee_id, extension)
    import os
    full_path = os.path.join(settings.UPLOAD_DIR, rel_path)
    ensure_dir(os.path.dirname(full_path))
    with open(full_path, "wb") as f:
        f.write(content)
    file_size = len(content)
    mime_type = file.content_type or "application/octet-stream"
    record = Record(
        id=str(uuid.uuid4()),
        type=rec_type,
        file_path=rel_path,
        file_size=file_size,
        mime_type=mime_type,
        shop_id=shop_id,
        employee_id=employee_id,
        uploaded_by=current_user.id,
    )
    db.add(record)
    make_log(db, current_user.id, "upload", {"record_id": record.id, "type": rec_type.value})
    db.commit()
    db.refresh(record)
    return _enrich_record(record, db)

@router.post("/no-bag", response_model=RecordOut)
def no_bag_record(data: RecordNoBag, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = Record(
        id=str(uuid.uuid4()),
        type=RecordType.no_bag,
        shop_id=data.shop_id,
        employee_id=data.employee_id,
        uploaded_by=current_user.id,
    )
    db.add(record)
    make_log(db, current_user.id, "no_bag", {"employee_id": data.employee_id})
    db.commit()
    db.refresh(record)
    return _enrich_record(record, db)

@router.get("", response_model=List[RecordOut])
def list_records(
    shop_id: Optional[str] = None,
    date_filter: Optional[str] = None,
    employee_id: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Record)
    if current_user.role == UserRole.shop_admin:
        q = q.filter(Record.shop_id == current_user.shop_id)
    elif shop_id:
        q = q.filter(Record.shop_id == shop_id)
    if employee_id:
        q = q.filter(Record.employee_id == employee_id)
    if type:
        q = q.filter(Record.type == type)
    if date_filter:
        try:
            d = date.fromisoformat(date_filter)
            day_start = datetime(d.year, d.month, d.day)
            day_end = datetime(d.year, d.month, d.day, 23, 59, 59)
            q = q.filter(Record.created_at >= day_start, Record.created_at <= day_end)
        except ValueError:
            pass
    records = q.order_by(Record.created_at.desc()).all()
    return [_enrich_record(r, db) for r in records]

@router.get("/{record_id}", response_model=RecordOut)
def get_record(record_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return _enrich_record(record, db)

@router.post("/{record_id}/check", response_model=RecordOut)
def check_record(record_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_director_or_above)):
    record = db.query(Record).filter(Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    record.checked_by = current_user.id
    record.checked_at = datetime.utcnow()
    make_log(db, current_user.id, "check", {"record_id": record_id})
    db.commit()
    db.refresh(record)
    return _enrich_record(record, db)

def _enrich_record(record: Record, db: Session) -> RecordOut:
    from ..models.employee import Employee
    from ..models.user import User as UserModel
    emp = db.query(Employee).filter(Employee.id == record.employee_id).first()
    uploader = db.query(UserModel).filter(UserModel.id == record.uploaded_by).first()
    out = RecordOut.model_validate(record)
    out.employee_name = emp.full_name if emp else None
    out.uploader_name = uploader.full_name if uploader else None
    return out
