from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel

router = APIRouter()

SECRET = "supersecret"

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class UserCreate(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed = pwd_context.hash(user.password[:72])
        new_user = User(email=user.email, password=hashed)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"msg": "Usuário criado"}

    except Exception as e:
        return {"error": str(e)}

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not pwd_context.verify(user.password[:72], db_user.password):
        return {"error": "Credenciais inválidas"}

    token = jwt.encode({"user_id": db_user.id}, SECRET, algorithm="HS256")

    return {"token": token}