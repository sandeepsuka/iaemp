from fastapi import APIRouter, Depends, Response, Form, HTTPException
from sqlalchemy.orm import sessionmaker

from app.database import engine
from app.models import Admin, ContactMessage, Membership
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.deps import admin_required

SessionLocal = sessionmaker(bind=engine)

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)

# ===============================
# ADMIN LOGIN (PUBLIC)
# ===============================
@router.post("/login")
def admin_login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()
    admin = db.query(Admin).filter(Admin.email == email).first()

    if not admin or not verify_password(password, admin.password_hash):
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
# ADMIN AUTH CHECK
# ===============================
@router.get("/me")
def admin_me(admin_email: str = Depends(admin_required)):
    return {"email": admin_email}


# ===============================
# ADMIN DASHBOARD (TEST)
# ===============================
@router.get("/dashboard")
def admin_dashboard(admin_email: str = Depends(admin_required)):
    return {"message": "admin access granted"}


# ===============================
# ADMIN DATA
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
# ADMIN LOGOUT
# ===============================
@router.post("/logout")
def admin_logout(response: Response):
    response.delete_cookie(
        key="admin_token",
        path="/"
    )
    return {"message": "logged out"}
