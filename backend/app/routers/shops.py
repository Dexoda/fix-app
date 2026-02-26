from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.shop import Shop
from ..schemas.shop import ShopCreate, ShopUpdate, ShopOut
from ..dependencies.permissions import require_super_admin
from ..dependencies.auth import get_current_user
import uuid

router = APIRouter(prefix="/shops", tags=["shops"])

@router.get("", response_model=List[ShopOut])
def list_shops(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Shop).all()

@router.post("", response_model=ShopOut)
def create_shop(data: ShopCreate, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    shop = Shop(id=str(uuid.uuid4()), name=data.name, address=data.address)
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop

@router.put("/{shop_id}", response_model=ShopOut)
def update_shop(shop_id: str, data: ShopUpdate, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(shop, field, value)
    db.commit()
    db.refresh(shop)
    return shop

@router.delete("/{shop_id}")
def delete_shop(shop_id: str, db: Session = Depends(get_db), _: User = Depends(require_super_admin)):
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    db.delete(shop)
    db.commit()
    return {"ok": True}
