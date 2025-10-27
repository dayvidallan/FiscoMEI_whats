
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .services import (
    get_or_seed_plans, find_user_by_phone, increment_usage, within_limits,
    send_wa_text, parse_intent_simple, call_openai_extract, create_finance_entry
)
from .models import MensagemLog

VERIFY_TOKEN = getattr(settings, "WA_VERIFY_TOKEN", "fiscoMEI_XHJD_2025")

@require_http_methods(["GET"])
def webhook_verify(request):
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        get_or_seed_plans()
        return HttpResponse(challenge or "", status=200)
    return HttpResponse("Verification failed", status=403)

@csrf_exempt
@require_http_methods(["POST"])
def webhook_receive(request):
    data = json.loads(request.body.decode() or "{}")
    try:
        entry = (data.get("entry") or [])[0]
        change = (entry.get("changes") or [])[0]
        value = change.get("value", {})
        messages = value.get("messages", [])
        if not messages:
            return HttpResponse("EVENT_RECEIVED", status=200)
        msg = messages[0]
        from_wa = msg.get("from")
        mtype = msg.get("type","text")
        text = ""
        if mtype == "text":
            text = msg.get("text",{}).get("body","").strip()

        MensagemLog.objects.create(telefone=from_wa, tipo=mtype, conteudo=text)

        # mapear telefone -> user
        user = find_user_by_phone(from_wa)
        if not user:
            send_wa_text(from_wa, "🚫 Número não cadastrado no FiscoMEI. Acesse o painel e associe seu WhatsApp.")
            return HttpResponse("EVENT_RECEIVED", status=200)

        # controle de uso/planos
        uso = increment_usage(user)
        ok, flag = within_limits(uso)
        if not ok:
            send_wa_text(from_wa, "🚫 Você atingiu o limite do seu plano. Renove para continuar: https://mei.sistemasfisco.com.br/planos")
            return HttpResponse("EVENT_RECEIVED", status=200)
        if flag == "soft":
            send_wa_text(from_wa, "⚠️ Uso intenso neste mês; você está perto do limite do seu plano.")

        # IA: extrair intenções
        extracted = call_openai_extract(text) or parse_intent_simple(text)

        if not extracted.get("valor") and extracted.get("tipo") in ("entrada","saida"):
            send_wa_text(from_wa, "Não consegui identificar o valor. Ex.: 'vendi por 250,00 hoje'")
            return HttpResponse("EVENT_RECEIVED", status=200)

        if extracted.get("tipo") in ("entrada","saida"):
            r = create_finance_entry(user, extracted)
            if r.get("ok"):
                send_wa_text(from_wa, f"{'Receita' if extracted['tipo']=='entrada' else 'Despesa'} registrada ✅. Fonte: {r.get('fonte')}")
            else:
                send_wa_text(from_wa, "Não consegui registrar, tente novamente com outro formato.")
        else:
            # comandos simples
            low = text.lower()
            if "saldo" in low or "relatório" in low or "relatorio" in low:
                send_wa_text(from_wa, "📊 Relatórios por aqui em breve. Por enquanto, acesse o painel para filtrar PDF.")
            else:
                send_wa_text(from_wa, "Entendi. Você pode dizer: 'vendi X por 500 hoje' ou 'gastei 80 em material'.")

        return HttpResponse("EVENT_RECEIVED", status=200)
    except Exception:
        return HttpResponse("EVENT_RECEIVED", status=200)
