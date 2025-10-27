
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO
from datetime import datetime

def generate_receipt_pdf(sale):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(30*mm, (h - 30*mm), "RECIBO - FiscoMEI")
    c.setFont("Helvetica", 11)
    y = h - 45*mm

    lines = [
        f"Cliente: {sale.customer_name}",
        f"Produto/Serviço: {sale.product_name}",
        f"Valor: R$ {sale.value:.2f}",
        f"Data da venda: {sale.date.strftime('%d/%m/%Y')}",
        f"Nº interno: {sale.id}",
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
    ]
    for line in lines:
        c.drawString(30*mm, y, line)
        y -= 8*mm

    c.line(30*mm, y, w - 30*mm, y)
    y -= 10*mm
    c.drawString(30*mm, y, "Assinatura: _______________________________")

    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    sale.receipt_pdf.save(f"recibo_{sale.id}.pdf", ContentFile(pdf_bytes), save=True)
    return sale.receipt_pdf.url
