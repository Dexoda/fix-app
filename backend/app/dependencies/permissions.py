from fastapi import Depends, HTTPException, status
from .auth import get_current_user
from ..models.user import User, UserRole

def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.super_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Super admin required")
    return current_user

def require_director_or_above(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in (UserRole.super_admin, UserRole.director):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Director role required")
    return current_user

def require_shop_admin_or_above(current_user: User = Depends(get_current_user)) -> User:
    return current_user
