
import re
from datetime import datetime

def parse_currency(txt: str):
    # Aceita "120", "120.50", "120,50", "R$ 120,50"
    m = re.search(r'(?:r\$\s*)?(\d+[\.,]?\d{0,2})', txt, flags=re.IGNORECASE)
    if not m: return None
    val = m.group(1).replace('.', '').replace(',', '.')
    try:
        return float(val)
    except:
        return None

def parse_date(txt: str):
    # dd/mm/aaaa ou dd-mm-aaaa
    m = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', txt)
    if not m: return None
    d, mth, y = map(int, m.groups())
    if y < 100: y += 2000
    try:
        return datetime(y, mth, d).date()
    except:
        return None

def extract_sale(text: str):
    # Heurística simples: "venda ... cliente X ... produto Y ... valor Z ... data D"
    t = text.lower()
    if 'venda' not in t: return None
    # nome cliente
    cliente = None
    m = re.search(r'cliente[:=]?\s*(.+?)(?:;|\n|,|\sproduto|\svalor|\sdata|$)', text, flags=re.IGNORECASE)
    if m: cliente = m.group(1).strip()

    # produto
    produto = None
    m = re.search(r'(?:produto|item|servi[cç]o)[:=]?\s*(.+?)(?:;|\n|,|\svalor|\sdata|$)', text, flags=re.IGNORECASE)
    if m: produto = m.group(1).strip()

    # valor
    valor = parse_currency(text)

    # data
    data = parse_date(text)

    return {'customer_name': cliente, 'product_name': produto, 'value': valor, 'date': data}

def extract_expense(text: str):
    # "saída ... categoria X ... descricao Y ... valor Z ... data D"
    t = text.lower()
    if 'saída' not in t and 'saida' not in t: return None
    cat = None
    m = re.search(r'(?:categoria|tipo)[:=]?\s*(.+?)(?:;|\n|,|\sdescri[cç][aã]o|\svalor|\sdata|$)', text, flags=re.IGNORECASE)
    if m: cat = m.group(1).strip()
    desc = None
    m = re.search(r'(?:descri[cç][aã]o|obs)[:=]?\s*(.+?)(?:;|\n|,|\svalor|\sdata|$)', text, flags=re.IGNORECASE)
    if m: desc = m.group(1).strip()
    valor = parse_currency(text)
    data = parse_date(text)
    return {'category': cat, 'description': desc, 'value': valor, 'date': data}
import re
from datetime import datetime, date

currency = r"(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2}|\d+(?:[.,]\d{2})?)"

def parse_money(txt):
    m = re.search(currency, txt)
    if not m: return None
    v = m.group(1).replace(".", "").replace(",", ".")
    return round(float(v), 2)

def parse_date(txt):
    m = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", txt)
    if m:
        d, mth, y = map(int, m.groups())
        y = y + 2000 if y < 100 else y
        try: return date(y, mth, d)
        except: pass
    if re.search(r"\b(hoje|agora|hj)\b", txt, re.I):
        return date.today()
    return None

def extract_name(label, txt):
    # ex: "cliente Ana Clara", "produto Brownie"
    m = re.search(fr"{label}\s*[:\-]?\s*([^\n;|,]+)", txt, re.I)
    return m.group(1).strip() if m else None

def detect_intent(txt):
    t = txt.lower()
    if re.search(r"\b(venda|vendi|registrar venda)\b", t): return "venda"
    if re.search(r"\b(sa[ií]da|despesa|gastei|lançar sa[ií]da)\b", t): return "saida"
    if re.search(r"\b(recibo|gerar recibo)\b", t): return "recibo"
    if re.search(r"\b(ajuda|help|menu)\b", t): return "ajuda"
    return "desconhecido"

def parse_sale(txt):
    return {
        "cliente": extract_name("cliente", txt),
        "produto": extract_name("produto", txt),
        "valor": parse_money(txt),
        "data": parse_date(txt) or date.today(),
    }

def parse_expense(txt):
    return {
        "descricao": extract_name("descri[cç][aã]o|item|motivo", txt) or extract_name("saida", txt),
        "valor": parse_money(txt),
        "data": parse_date(txt) or date.today(),
    }
