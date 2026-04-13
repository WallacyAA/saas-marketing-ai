from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Clinic, Post
from pydantic import BaseModel

router = APIRouter()

class ClinicCreate(BaseModel):
    name: str
    owner_id: int
    whatsapp_number: str | None = None
    welcome_message: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/clinic")
def create_clinic(clinic: ClinicCreate, db: Session = Depends(get_db)):
    new_clinic = Clinic(
        name=clinic.name,
        owner_id=clinic.owner_id,
        whatsapp_number=clinic.whatsapp_number,
        welcome_message=clinic.welcome_message
    )
    db.add(new_clinic)
    db.commit()
    db.refresh(new_clinic)
    return {"msg": "Clínica criada", "clinic_id": new_clinic.id}

@router.get("/posts/{clinic_id}")
def get_posts(clinic_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.clinic_id == clinic_id).all()
    return posts

@router.get("/clinic/{clinic_id}")
def get_clinic(clinic_id: int, db: Session = Depends(get_db)):
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()
    if not clinic:
        return {"error": "Clínica não encontrada"}
    return clinic