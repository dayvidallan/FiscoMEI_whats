import os, json, requests, re
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

WA_VERIFY_TOKEN    = os.getenv("WA_VERIFY_TOKEN", "fiscoMEI_XHJD_2025")
WA_TOKEN           = os.getenv("WA_TOKEN", "")
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID", "")
WA_API_VERSION     = os.getenv("WA_API_VERSION", "v21.0")

def verify(request):
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")
    if mode == "subscribe" and token == WA_VERIFY_TOKEN:
        return HttpResponse(challenge or "", status=200)
    return HttpResponse("Erro de verificação", status=403)

@csrf_exempt
def receive(request):
    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        data = {}

    try:
        entry = (data.get("entry") or [])[0]
        change = (entry.get("changes") or [])[0]
        value = change.get("value", {})
        messages = value.get("messages", [])
        if not messages:
            return HttpResponse("EVENT_RECEIVED", status=200)

        message = messages[0]
        wa_from = message.get("from")
        mtype   = message.get("type")

        if mtype == "text":
            body = (message.get("text") or {}).get("body", "").strip()
            if body.lower().startswith("venda"):
                parsed = parse_kv_pairs(body)
                with transaction.atomic():
                    recibo_url = gerar_recibo_url_mock(parsed)
                send_text(wa_from, f"✅ Venda registrada! Recibo: {recibo_url}")
            else:
                send_text(wa_from,
                    "Olá! Para registrar venda, envie:\\n"
                    "venda;cliente=Nome;produto=Descrição;valor=99.90;data=AAAA-MM-DD")
        else:
            send_text(wa_from, "Recebi sua mensagem! Em breve suportaremos anexos e áudio.")

        return HttpResponse("EVENT_RECEIVED", status=200)
    except Exception:
        return HttpResponse("EVENT_RECEIVED", status=200)

def send_text(to, text):
    if not (WA_TOKEN and WA_PHONE_NUMBER_ID):
        return
    url = f"https://graph.facebook.com/{WA_API_VERSION}/{WA_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    try:
        requests.post(url, headers=headers, json=payload, timeout=15)
    except Exception:
        pass

def parse_kv_pairs(text):
    parts = [p.strip() for p in text.split(";") if p.strip()]
    out = {}
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            out[k.strip().lower()] = v.strip()
    return out

def gerar_recibo_url_mock(parsed):
    nome = re.sub(r"[^a-z0-9]+", "-", (parsed.get("cliente","") or "cliente").lower())
    return f"https://mei.sistemasfisco.com.br/media/recibos/{nome}-preview.pdf"