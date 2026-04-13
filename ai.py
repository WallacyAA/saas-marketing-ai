from fastapi import APIRouter
from pydantic import BaseModel
from database import SessionLocal
from models import Post
from twilio.rest import Client
import os

router = APIRouter()

# Twilio
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = "whatsapp:+14155238886"
DESTINATION_NUMBER = "whatsapp:+559391724587"  # troque pelo seu número

twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

class PostRequest(BaseModel):
    topic: str

@router.post("/generate-post")
def generate_post(data: PostRequest):
    db = SessionLocal()

    try:
        post_content = f"""
🦷 Dica do dia sobre {data.topic}!

Manter bons hábitos é essencial para sua saúde.

✅ Escove os dentes após as refeições
✅ Use fio dental diariamente
✅ Visite seu dentista regularmente

Cuide do seu sorriso 😁✨
"""

        new_post = Post(content=post_content, clinic_id=1)
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