from fastapi import APIRouter, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

router = APIRouter()

user_states = {}

@router.post("/webhook-whatsapp")
def webhook_whatsapp(Body: str = Form(...), From: str = Form(...)):
    print(f"Mensagem de {From}: {Body}")

    texto = Body.strip().lower()
    resposta = ""

    # reinicia a conversa sempre que o usuário disser oi/olá
    if texto in ["oi", "olá", "ola", "menu", "início", "inicio"]:
        user_states[From] = {"etapa": "inicio"}
        resposta = "Olá! 😊 Sou o assistente da clínica. Você deseja agendar uma consulta ou saber valores?"

    else:
        estado = user_states.get(From, {})

        if not estado:
            if "consulta" in texto:
                resposta = "Perfeito! Qual tratamento você deseja? (ex: limpeza, clareamento, aparelho)"
                user_states[From] = {"etapa": "tratamento"}
            elif "valor" in texto or "preço" in texto:
                resposta = "Claro! Sobre qual tratamento você deseja saber o valor?"
                user_states[From] = {"etapa": "valor"}
            else:
                resposta = "Olá! Posso te ajudar com agendamento de consulta ou valores. Digite 'oi' para começar."
                user_states[From] = {"etapa": "inicio"}

        elif estado.get("etapa") == "inicio":
            if "consulta" in texto:
                resposta = "Perfeito! Qual tratamento você deseja? (ex: limpeza, clareamento, aparelho)"
                user_states[From] = {"etapa": "tratamento"}
            elif "valor" in texto or "preço" in texto:
                resposta = "Claro! Sobre qual tratamento você deseja saber o valor?"
                user_states[From] = {"etapa": "valor"}
            else:
                resposta = "Você deseja agendar uma consulta ou saber valores?"

        elif estado.get("etapa") == "tratamento":
            user_states[From]["tratamento"] = texto
            user_states[From]["etapa"] = "dia"
            resposta = "Ótimo! Qual dia você prefere?"

        elif estado.get("etapa") == "dia":
            user_states[From]["dia"] = texto
            user_states[From]["etapa"] = "nome"
            resposta = "Perfeito! Qual seu nome?"

        elif estado.get("etapa") == "nome":
            nome = texto
            tratamento = user_states[From].get("tratamento")
            dia = user_states[From].get("dia")

            resposta = f"Perfeito, {nome}! 😊 Sua solicitação de {tratamento} para o dia {dia} foi registrada. Em breve entraremos em contato!"
            user_states.pop(From, None)

        elif estado.get("etapa") == "valor":
            resposta = f"O valor do tratamento de {texto} pode variar. Podemos te passar mais detalhes. Deseja agendar uma avaliação?"
            user_states.pop(From, None)

        else:
            resposta = "Não entendi muito bem. Digite 'oi' para recomeçar."
            user_states.pop(From, None)

    twiml = MessagingResponse()
    twiml.message(resposta)

    return Response(content=str(twiml), media_type="application/xml")