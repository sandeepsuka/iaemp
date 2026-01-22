# ===============================
# ENV
# ===============================
from dotenv import load_dotenv
load_dotenv()

# ===============================
# IMPORTS
# ===============================
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker

from app.database import engine
from app.models import ContactMessage, Membership
from app.routes.admin import router as admin_router

# ===============================
# APP
# ===============================
app = FastAPI(
    title="IAEMP Backend API",
    docs_url=None,
    redoc_url=None
)

# ===============================
# ROUTES
# ===============================
app.include_router(admin_router)

# ===============================
# CORS (COOKIES SAFE)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# DB SESSION
# ===============================
SessionLocal = sessionmaker(bind=engine)

# ===============================
# HEALTH
# ===============================
@app.get("/api/health")
def health():
    return {"status": "ok"}

# ===============================
# CONTACT FORM (FORM OK)
# ===============================
@app.post("/api/contact")
def submit_contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    db = SessionLocal()
    db.add(ContactMessage(name=name, email=email, message=message))
    db.commit()
    db.close()
    return {"message": "submitted"}

# ===============================
# MEMBERSHIP FORM (FORM OK)
# ===============================
@app.post("/api/membership")
def submit_membership(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    membership_type: str = Form(...),
    organization: str = Form(None)
):
    db = SessionLocal()
    db.add(Membership(
        full_name=full_name,
        email=email,
        phone=phone,
        membership_type=membership_type,
        organization=organization
    ))
    db.commit()
    db.close()
    return {"message": "submitted"}
