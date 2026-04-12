from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Clinic
from pydantic import BaseModel
from models import Post

router = APIRouter()

class ClinicCreate(BaseModel):
    name: str
    owner_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/clinic")
def create_clinic(clinic: ClinicCreate, db: Session = Depends(get_db)):
    new_clinic = Clinic(name=clinic.name, owner_id=clinic.owner_id)
    db.add(new_clinic)
    db.commit()
    return {"msg": "Clínica criada"}

@router.get("/posts/{clinic_id}")
def get_posts(clinic_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.clinic_id == clinic_id).all()

    return posts