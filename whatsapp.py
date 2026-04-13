from fastapi import APIRouter
from pydantic import BaseModel
from twilio.rest import Client
import os

router = APIRouter()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = "whatsapp:+14155238886"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

class Message(BaseModel):
    to: str
    body: str

@router.post("/send-whatsapp")
def send_whatsapp(msg: Message):
    try:
        message = client.messages.create(
            from_=TWILIO_NUMBER,
            body=msg.body,
            to=f"whatsapp:{msg.to}"
        )
        return {"status": "enviado", "sid": message.sid}
    except Exception as e:
        return {"error": str(e)}