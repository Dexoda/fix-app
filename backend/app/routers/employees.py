from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.user import User, UserRole
from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeOut
from ..dependencies.permissions import require_super_admin
from ..dependencies.auth import get_current_user
import uuid

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("", response_model=List[EmployeeOut])
def list_employees(shop_id: Optional[str] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = db.query(Employee)
    if current_user.role == UserRole.shop_admin:
        q = q.filter(Employee.shop_id == current_user.shop_id)
    elif shop_id:
        q = q.filter(Employee.shop_id == shop_id)
    return q.all()

@router.post("", response_model=EmployeeOut)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    emp = Employee(id=str(uuid.uuid4()), full_name=data.full_name, shop_id=data.shop_id, position=data.position)
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

@router.put("/{emp_id}", response_model=EmployeeOut)
def update_employee(emp_id: str, data: EmployeeUpdate, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    db.commit()
    db.refresh(emp)
    return emp

@router.delete("/{emp_id}")
def delete_employee(emp_id: str, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()
    return {"ok": True}
