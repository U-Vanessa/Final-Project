from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.schemas.auth_schema import RegisterRequest

router = APIRouter()
ORG_DOMAIN = "@icttoolsasm.com"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-user")
def create_user(payload: RegisterRequest, db: Session = Depends(get_db)):

    if not payload.email.endswith(ORG_DOMAIN):
        raise HTTPException(status_code=400, detail="Use organization email")

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(payload.password)

    user = User(
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        department=payload.department,
        station=payload.station,
        password=hashed,
        role=payload.role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}


@router.get("/it-personnel")
def list_it_personnel(db: Session = Depends(get_db)):
    users = (
        db.query(User)
        .filter(User.role == "IT", User.is_active.is_(True))
        .order_by(User.created_at.desc())
        .all()
    )

    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "department": user.department,
            "station": user.station,
            "role": user.role,
        }
        for user in users
    ]