from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import Admin, ContactMessage, Membership
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.deps import admin_required

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)

# ===============================
# SCHEMA
# ===============================
class LoginRequest(BaseModel):
    email: str
    password: str

# ===============================
# ADMIN LOGIN (JSON)
# ===============================
@router.post("/login")
def admin_login(payload: LoginRequest, response: Response):
    db: Session = SessionLocal()

    admin = db.query(Admin).filter(Admin.email == payload.email).first()

    if not admin:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, admin.password_hash):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": admin.email})

    response.set_cookie(
        key="admin_token",
        value=token,
        httponly=True,
        samesite="lax",
        path="/"
    )

    db.close()
    return {"message": "login successful"}

# ===============================
# AUTH CHECK
# ===============================
@router.get("/me")
def admin_me(admin_email: str = Depends(admin_required)):
    return {"email": admin_email}

# ===============================
# DATA
# ===============================
@router.get("/contacts")
def admin_contacts(admin_email: str = Depends(admin_required)):
    db = SessionLocal()
    data = db.query(ContactMessage).all()
    db.close()
    return data

@router.get("/memberships")
def admin_memberships(admin_email: str = Depends(admin_required)):
    db = SessionLocal()
    data = db.query(Membership).all()
    db.close()
    return data

# ===============================
# LOGOUT
# ===============================
@router.post("/logout")
def admin_logout(response: Response):
    response.delete_cookie(key="admin_token", path="/")
    return {"message": "logged out"}
