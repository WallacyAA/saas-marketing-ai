from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from database import SessionLocal
from models import Post
from twilio.rest import Client
import os
import random

router = APIRouter()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = "whatsapp:+14155238886"
DESTINATION_NUMBER = "whatsapp:+559391724587"

twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

class PostRequest(BaseModel):
    topic: str

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

@router.post("/generate-post")
def generate_post(data: PostRequest):
    db = SessionLocal()

    try:
        post_content = f"""
{random.choice(aberturas)}

Tema de hoje: {data.topic}

{random.choice(corpos)}

{random.choice(chamadas)}
"""

        new_post = Post(
            content=post_content,
            clinic_id=1,
            created_at=datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        db.add(new_post)
        db.commit()

        message = twilio_client.messages.create(
            from_=TWILIO_NUMBER,
            body=post_content,
            to=DESTINATION_NUMBER
        )

        return {
            "post": post_content,
            "whatsapp_status": "enviado",
            "message_sid": message.sid
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()