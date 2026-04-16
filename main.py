from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
from models import Base, Post
from auth import router as auth_router
from clinic import router as clinic_router
from ai import router as ai_router
from whatsapp import router as whatsapp_router
from webhook_whatsapp import router as webhook_whatsapp_router
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    import random

    db = SessionLocal()

    temas = [
        "clareamento dental",
        "limpeza dental",
        "aparelho ortodôntico",
        "implantes dentários",
        "saúde bucal",
        "prevenção",
        "lentes em resina",
        "prótese dentária"
    ]

    aberturas = [
        "🦷 Seu sorriso merece cuidado especial!",
        "✨ Cuidar do sorriso é investir em autoestima.",
        "😁 Um sorriso bonito começa com bons hábitos.",
        "💙 Saúde bucal também é qualidade de vida.",
    ]

    corpos = [
        "Manter consultas regulares ajuda a prevenir problemas e manter a saúde da boca em dia.",
        "Pequenos cuidados diários fazem toda a diferença para ter dentes mais saudáveis e bonitos.",
        "A prevenção é sempre o melhor caminho para evitar desconfortos e tratamentos mais complexos.",
        "Com o acompanhamento certo, você conquista mais segurança para sorrir e falar com confiança.",
    ]

    chamadas = [
        "Agende sua avaliação e cuide do seu sorriso hoje mesmo!",
        "Entre em contato e descubra o melhor tratamento para você.",
        "Sua saúde bucal merece atenção. Fale com nossa equipe!",
        "Estamos prontos para te ajudar a sorrir com mais confiança.",
    ]

    tema = random.choice(temas)

    post_content = f"""
{random.choice(aberturas)}

Tema de hoje: {tema}

{random.choice(corpos)}

{random.choice(chamadas)}
"""

    print("Gerando post automático...")

    post = Post(
        content=post_content,
        clinic_id=1
    )

    db.add(post)
    db.commit()
    db.close()

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