# app.py
import os
import json
import logging
from flask import Flask, request, jsonify
import requests

# ------------------------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------------------------
# Defina no ambiente (Render → Environment → Environment Variables, ou local)
#   WA_TOKEN        = token de acesso (gerado na tela "Gerar token de acesso")
#   WA_PHONE_ID     = ID do número do WhatsApp Business (ex.: 892310547290928)
#   WA_VERIFY_TOKEN = token que você coloca no painel da Meta p/ validar webhook
WA_TOKEN        = os.getenv("WA_TOKEN", "").strip()
WA_PHONE_ID     = os.getenv("WA_PHONE_ID", "").strip()
WA_VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN", "fiscoMEI_XHJD_2025").strip()

GRAPH_URL = f"https://graph.facebook.com/v20.0/{WA_PHONE_ID}/messages"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

app = Flask(__name__)

# ------------------------------------------------------------------------------
# HEALTHCHECK
# ------------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def root():
    return "Servidor Flask ativo 🚀", 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify(ok=True), 200

# ------------------------------------------------------------------------------
# WEBHOOK VERIFY (GET)
# ------------------------------------------------------------------------------
@app.route("/webhooks/whatsapp", methods=["GET"])
def verify_webhook():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == WA_VERIFY_TOKEN:
        logging.info("✅ Webhook verificado com sucesso.")
        # O Facebook espera que retornemos APENAS o challenge como texto
        return challenge, 200
    else:
        logging.error("❌ Falha na verificação do webhook (token inválido ou mode ausente).")
        return "Erro de verificação", 403

# ------------------------------------------------------------------------------
# WEBHOOK RECEIVE (POST)
# ------------------------------------------------------------------------------
@app.route("/webhooks/whatsapp", methods=["POST"])
def receive_message():
    data = request.get_json(silent=True, force=True) or {}
    logging.info(f"📩 Incoming webhook: {json.dumps(data, ensure_ascii=False)}")

    try:
        entries = data.get("entry", [])
        for entry in entries:
            changes = entry.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                if not messages:
                    continue

                for msg in messages:
                    sender_wa_id = msg.get("from")            # ex.: "5584...."
                    msg_type     = msg.get("type")

                    # Extrai o texto, se houver
                    user_text = ""
                    if msg_type == "text":
                        user_text = (msg.get("text") or {}).get("body", "")

                    # Monte a resposta simples (eco)
                    reply = f"Recebido: {user_text or '(sem texto)'}"
                    send_text_message(sender_wa_id, reply)
        return "EVENT_RECEIVED", 200

    except Exception as e:
        logging.exception(f"Erro processando webhook: {e}")
        return "ERROR", 500

# ------------------------------------------------------------------------------
# SEND MESSAGE
# ------------------------------------------------------------------------------
def send_text_message(to_wa_id: str, text: str):
    if not (WA_TOKEN and WA_PHONE_ID):
        logging.warning("⚠️ WA_TOKEN/WA_PHONE_ID não configurados; não dá para enviar mensagem.")
        return

    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_wa_id,
        "type": "text",
        "text": {"body": text}
    }

    try:
        resp = requests.post(GRAPH_URL, headers=headers, json=payload, timeout=30)
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        logging.info(f"📤 WA send resp: {resp.status_code} {body}")
    except Exception as e:
        logging.exception(f"Erro enviando mensagem: {e}")

# ------------------------------------------------------------------------------
# MAIN (para rodar localmente; no Render use gunicorn: `gunicorn app:app`)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # debug=False para se comportar igual produção; porta 5000 por padrão
    app.run(host="0.0.0.0", port=5000, debug=False)

import os
from flask import Flask, request

app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("WA_VERIFY_TOKEN", "fiscoMEI_XHJD_2025")

@app.get("/")
def home():
    return "Servidor Flask ativo 🚀", 200

@app.get("/webhooks/whatsapp")
def verify_token():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Erro de verificação", 403

@app.post("/webhooks/whatsapp")
def receive_message():
    data = request.get_json()
    print("📩 Mensagem recebida:", data)
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
