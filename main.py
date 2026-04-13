from fastapi import FastAPI
from database import engine, SessionLocal
from models import Base, Post
from auth import router as auth_router
from clinic import router as clinic_router
from ai import router as ai_router
from apscheduler.schedulers.background import BackgroundScheduler
from whatsapp import router as whatsapp_router
from webhook_whatsapp import router as webhook_whatsapp_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(clinic_router)
app.include_router(ai_router)
app.include_router(whatsapp_router)
app.include_router(webhook_whatsapp_router)

@app.get("/")
def home():
    return {"msg": "API rodando 🚀"}


def gerar_post_automatico():
    db = SessionLocal()

    print("Gerando post automático...")

    post = Post(
        content="🦷 Dica diária automática: não esqueça de escovar os dentes!",
        clinic_id=1
    )

    db.add(post)
    db.commit()
    db.close()


scheduler = BackgroundScheduler()

@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(gerar_post_automatico, "interval", seconds=30)
    scheduler.start()