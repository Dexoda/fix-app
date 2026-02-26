from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.log import Log
from ..models.user import User
from ..schemas.log import LogOut
from ..dependencies.permissions import require_super_admin

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("", response_model=List[LogOut])
def list_logs(db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    logs = db.query(Log).order_by(Log.created_at.desc()).limit(500).all()
    result = []
    for log in logs:
        out = LogOut.model_validate(log)
        if log.user:
            out.user_name = log.user.full_name
        result.append(out)
    return result
