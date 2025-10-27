import requests
import mimetypes
from django.conf import settings

API = "https://graph.facebook.com/v21.0"

def _headers():
    return {"Authorization": f"Bearer {settings.WHATS_TOKEN}"}

def send_text(to, body):
    data = {"messaging_product":"whatsapp","to": to,"type":"text","text":{"body": body}}
    r = requests.post(f"{API}/{settings.WHATS_PHONE_ID}/messages", json=data, headers=_headers(), timeout=30)
    r.raise_for_status()

def send_document(to, url, filename="recibo.pdf", caption=None):
    data = {
        "messaging_product":"whatsapp","to":to,"type":"document",
        "document":{"link": url, "filename": filename, **({"caption": caption} if caption else {})}
    }
    r = requests.post(f"{API}/{settings.WHATS_PHONE_ID}/messages", json=data, headers=_headers(), timeout=30)
    r.raise_for_status()

def get_media_url(media_id: str) -> str:
    r = requests.get(f"{API}/{media_id}", headers=_headers(), timeout=30)
    r.raise_for_status()
    return r.json()["url"]

def download_media(media_id: str) -> bytes:
    url = get_media_url(media_id)
    r = requests.get(url, headers=_headers(), timeout=60)
    r.raise_for_status()
    return r.content
