from fastapi import APIRouter, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

@router.post("/webhook-whatsapp")
def webhook_whatsapp(Body: str = Form(...), From: str = Form(...)):
    texto = Body.strip().lower()

    if "consulta" in texto:
        resposta = "Olá! Podemos agendar sua consulta. Qual dia e horário você prefere?"
    elif "preço" in texto or "valor" in texto:
        resposta = "Posso te ajudar com os valores. Qual tratamento você deseja saber?"
    elif "oi" in texto or "olá" in texto or "ola" in texto:
        resposta = "Olá! Seja bem-vindo. Como posso te ajudar hoje?"
    else:
        resposta = "Recebi sua mensagem. Pode me explicar melhor o que você precisa?"

    twiml = MessagingResponse()
    twiml.message(resposta)

    return Response(content=str(twiml), media_type="application/xml")