from fastapi import APIRouter, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from database import SessionLocal
from models import Clinic

router = APIRouter()

user_states = {}

@router.post("/webhook-whatsapp")
def webhook_whatsapp(Body: str = Form(...), From: str = Form(...)):
    db = SessionLocal()
    clinic = db.query(Clinic).filter(Clinic.id == 1).first()

    texto = Body.strip().lower()
    print(f"Mensagem recebida de {From}: {texto}")

    if texto in ["oi", "olá", "ola", "menu", "inicio", "início", "começar", "comecar"]:
        user_states[From] = {"etapa": "inicio"}
        resposta = clinic.welcome_message if clinic and clinic.welcome_message else "Olá! 😊 Como posso ajudar?"

    else:
        estado = user_states.get(From, {}).get("etapa")

        if estado is None:
            if "consulta" in texto or "agendar" in texto:
                user_states[From] = {"etapa": "tratamento"}
                resposta = "Perfeito! Qual tratamento você deseja? Ex.: limpeza, clareamento ou aparelho."
            elif "valor" in texto or "preço" in texto or "preco" in texto:
                user_states[From] = {"etapa": "valor"}
                resposta = "Claro! Sobre qual tratamento você deseja saber o valor?"
            else:
                user_states[From] = {"etapa": "inicio"}
                resposta = clinic.welcome_message if clinic and clinic.welcome_message else "Olá! 😊 Posso te ajudar com agendamento de consulta ou valores. Digite 'consulta' ou 'valor'."

        elif estado == "inicio":
            if "consulta" in texto or "agendar" in texto:
                user_states[From] = {"etapa": "tratamento"}
                resposta = "Perfeito! Qual tratamento você deseja? Ex.: limpeza, clareamento ou aparelho."
            elif "valor" in texto or "preço" in texto or "preco" in texto:
                user_states[From] = {"etapa": "valor"}
                resposta = "Claro! Sobre qual tratamento você deseja saber o valor?"
            else:
                resposta = "Você deseja agendar uma consulta ou saber valores?"

        elif estado == "tratamento":
            user_states[From]["tratamento"] = texto
            user_states[From]["etapa"] = "dia"
            resposta = "Ótimo! Qual dia você prefere?"

        elif estado == "dia":
            user_states[From]["dia"] = texto
            user_states[From]["etapa"] = "nome"
            resposta = "Perfeito! Qual seu nome?"

        elif estado == "nome":
            nome = texto
            tratamento = user_states[From].get("tratamento", "tratamento informado")
            dia = user_states[From].get("dia", "dia informado")

            resposta = f"Perfeito, {nome}! 😊 Sua solicitação de {tratamento} para o dia {dia} foi registrada. Em breve entraremos em contato!"
            user_states.pop(From, None)

        elif estado == "valor":
            resposta = f"O valor do tratamento de {texto} pode variar. Podemos te passar mais detalhes. Deseja agendar uma avaliação?"
            user_states.pop(From, None)

        else:
            user_states.pop(From, None)
            resposta = "Não entendi muito bem. Digite 'oi' para recomeçar."

    twiml = MessagingResponse()
    twiml.message(resposta)
    db.close()
    return Response(content=str(twiml), media_type="application/xml")