# FiscoMEI — Opção A (Django único)

Webhook WhatsApp: `/webhooks/whatsapp/` (GET validação, POST mensagens)

Render
Build:
    pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
Start:
    gunicorn fiscomei.wsgi:application --timeout 120

Env:
- SECRET_KEY, DEBUG=False
- WA_VERIFY_TOKEN, WA_TOKEN, WA_PHONE_NUMBER_ID, WA_API_VERSION
- DATABASE_URL (Postgres)
- ALLOWED_HOSTS