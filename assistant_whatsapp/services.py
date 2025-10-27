
import os, json, datetime, re
import requests
from decimal import Decimal
from django.conf import settings
from .models import Plano, UsoMensal, MensagemLog, LancamentoEspelho

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("ASSISTANT_MODEL", "gpt-4o-mini")
WA_TOKEN = os.getenv("WA_TOKEN", "")
WA_PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID", "")
WA_API_VERSION = os.getenv("WA_API_VERSION", "v21.0")

FAIR_USE_MULTIPLIER = 1.0  # já usamos o limite do plano como limite duro

MONEY_RE = re.compile(r"(?:R\$\s*|\b)(\d{1,3}(?:[\.\,]\d{3})*(?:[\,\.]\d{2})|\d+(?:[\,\.]\d{2}))")
DATE_RE = re.compile(r"(\d{1,2}/\d{1,2}/\d{2,4})")
CPF_RE = re.compile(r"(\d{3}\.\d{3}\.\d{3}-\d{2}|\b\d{11}\b)")
CNPJ_RE = re.compile(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\b\d{14}\b)")

def get_or_seed_plans():
    defaults = [
        {"nome":"Básico","limite_mensal":200,"preco":"49.90","descricao":"Até 200 mensagens por mês."},
        {"nome":"Pro","limite_mensal":500,"preco":"89.90","descricao":"Até 500 mensagens por mês."},
        {"nome":"Ilimitado","limite_mensal":2000,"preco":"129.90","descricao":"Uso justo até 2.000 mensagens/mês."},
    ]
    created = []
    for d in defaults:
        p, _ = Plano.objects.get_or_create(nome=d["nome"], defaults=d)
        created.append(p)
    return created

def find_user_by_phone(phone: str):
    """Localiza o user pelo telefone associado ao MEI (ajuste o import conforme seu projeto)."""
    try:
        from apps.mei.models import MEI
        mei = MEI.objects.filter(telefone__icontains=phone).select_related("user").first()
        if mei and mei.user_id:
            return mei.user
    except Exception:
        pass
    # fallback: tentar no próprio User (campo telefone se existir)
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.filter(telefone__icontains=phone).first()
        if user:
            return user
    except Exception:
        pass
    return None

def current_month():
    return datetime.date.today().strftime("%Y-%m")

def increment_usage(user):
    mes = current_month()
    # plano padrão: Básico
    plan = Plano.objects.filter(nome="Básico").first() or get_or_seed_plans()[0]
    uso, _ = UsoMensal.objects.get_or_create(user=user, mes=mes, defaults={"plano": plan, "mensagens": 0})
    uso.mensagens += 1
    uso.save()
    return uso

def within_limits(uso):
    limite_duro = int(uso.plano.limite_mensal * FAIR_USE_MULTIPLIER)
    near = int(limite_duro * 0.9)
    if uso.mensagens > limite_duro:
        return False, "hard"
    if uso.mensagens >= near:
        return True, "soft"
    return True, None

def send_wa_text(to, text):
    if not (WA_TOKEN and WA_PHONE_NUMBER_ID):
        return
    url = f"https://graph.facebook.com/{WA_API_VERSION}/{WA_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WA_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text[:4096]}}
    requests.post(url, headers=headers, json=payload, timeout=30)

def parse_intent_simple(text: str):
    """Regra rápida de fallback (caso a API da OpenAI não esteja setada)."""
    t = text.lower()
    tipo = None
    if any(k in t for k in ["gastei","paguei","despesa","saída","saida"]):
        tipo = "saida"
    if any(k in t for k in ["vendi","recebi","entrada","faturamento","receita","pix"]):
        tipo = "entrada"
    m = MONEY_RE.search(text)
    valor = None
    if m:
        raw = m.group(1).replace(".", "").replace(",", ".")
        try:
            valor = Decimal(raw)
        except Exception:
            valor = None
    d = None
    dm = DATE_RE.search(text)
    if dm:
        try:
            dd, mm, yy = dm.group(1).split("/")
            yy = ("20"+yy) if len(yy)==2 else yy
            d = datetime.date(int(yy), int(mm), int(dd))
        except Exception:
            d = datetime.date.today()
    else:
        d = datetime.date.today()
    cpf_cnpj = None
    cm = CNPJ_RE.search(text) or CPF_RE.search(text)
    if cm:
        cpf_cnpj = cm.group(1)
    descricao = text
    return {"tipo": tipo, "valor": valor, "data": d, "cpf_cnpj": cpf_cnpj, "descricao": descricao}

def call_openai_extract(text: str):
    if not OPENAI_API_KEY:
        return None
    try:
        import requests
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}","Content-Type":"application/json"}
        sys = "Você extrai campos financeiros: tipo(entrada/saida), valor, data(YYYY-MM-DD), pagador/opcional, cpf_cnpj/opcional, descricao."
        user = f"Texto: {text}"
        body = {"model": OPENAI_MODEL, "messages":[{"role":"system","content":sys},{"role":"user","content":user}],
                "response_format":{"type":"json_object"},
                "temperature":0.1}
        r = requests.post(url, headers=headers, json=body, timeout=30)
        r.raise_for_status()
        j = r.json()
        content = j["choices"][0]["message"]["content"]
        data = json.loads(content)
        # normaliza
        if "valor" in data:
            try:
                data["valor"] = Decimal(str(data["valor"]))
            except Exception:
                pass
        if "data" in data and isinstance(data["data"], str):
            try:
                y, m, d = map(int, data["data"].split("-"))
                data["data"] = datetime.date(y, m, d)
            except Exception:
                data["data"] = datetime.date.today()
        return data
    except Exception:
        return None


def create_finance_entry(user, payload):
    """Cria lançamento financeiro real no app.finance.Transaction."""
    from decimal import Decimal
    from apps.finance.models import Transaction
    from .models import LancamentoEspelho
    import datetime as _dt

    tipo = payload.get("tipo")
    valor = payload.get("valor")
    data = payload.get("data") or _dt.date.today()
    descricao = (payload.get("descricao") or "").strip()
    categoria = (payload.get("categoria") or "").strip()

    try:
        tx = Transaction.objects.create(
            kind="IN" if tipo == "entrada" else "OUT",
            date=data,
            description=descricao[:200],
            category=categoria[:80],
            amount=Decimal(str(valor)) if valor is not None else Decimal("0.00"),
        )
        return {"ok": True, "id": tx.id, "fonte": "finance.Transaction"}
    except Exception:
        # fallback espelho local para não perder o dado
        cents = int(Decimal(str(valor or 0)) * 100)
        le = LancamentoEspelho.objects.create(
            user=user,
            tipo=tipo or "entrada",
            valor_centavos=cents,
            descricao=descricao,
            data=data,
            origem="",
            cpf_cnpj="",
        )
        return {"ok": True, "id": le.id, "fonte": "assistant_whatsapp.LancamentoEspelho"}

