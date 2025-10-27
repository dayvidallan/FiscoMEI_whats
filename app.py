import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN", "fiscoMEI_XHJD_2025")
WA_TOKEN = os.getenv("WA_TOKEN", "")
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID", "")
WA_API_VERSION = os.getenv("WA_API_VERSION", "v21.0")

@app.get("/")
def home():
    return "OK - FiscoMEI API 🚀", 200

@app.get("/health")
def health():
    return jsonify(ok=True), 200

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
    data = request.get_json() or {}
    app.logger.info(f"Webhook recebido: {json.dumps(data, ensure_ascii=False)}")
    try:
        entry = (data.get("entry") or [])[0]
        change = (entry.get("changes") or [])[0]
        value = change.get("value", {})
        messages = value.get("messages", [])
        if not messages:
            return "EVENT_RECEIVED", 200
        message = messages[0]
        from_wa = message.get("from")
        msg_type = message.get("type")
        if msg_type == "text":
            body = message["text"]["body"]
            send_text(from_wa, f"Você disse: {body}")
        return "EVENT_RECEIVED", 200
    except Exception:
        app.logger.exception("Erro ao processar webhook")
        return "EVENT_RECEIVED", 200

def send_text(to, text):
    if not WA_TOKEN or not WA_PHONE_NUMBER_ID:
        app.logger.warning("WA_TOKEN ou WA_PHONE_NUMBER_ID não configurados.")
        return
    url = f"https://graph.facebook.com/{WA_API_VERSION}/{WA_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    import requests
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    app.logger.info(f"Envio WA: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
