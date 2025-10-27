from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import ModelForm, DateInput, Form, ChoiceField, CharField, DateField
from django.db.models import Sum, Q
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
import io

from .models import Transaction, Company

class TxForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['kind','date','category','description','amount']
        widgets = {'date': DateInput(attrs={'type':'date'})}

class FilterForm(Form):
    inicio = DateField(required=False, widget=DateInput(attrs={'type':'date'}))
    fim = DateField(required=False, widget=DateInput(attrs={'type':'date'}))
    kind = ChoiceField(required=False, choices=(('','Todos'),('IN','Entrada'),('OUT','Saída')))
    category = CharField(required=False)
    q = CharField(required=False)

def _apply_filters(qs, data):
    if not data: return qs
    if data.get('inicio'): qs = qs.filter(date__gte=data['inicio'])
    if data.get('fim'): qs = qs.filter(date__lte=data['fim'])
    if data.get('kind'): qs = qs.filter(kind=data['kind'])
    if data.get('category'): qs = qs.filter(category__icontains=data['category'])
    if data.get('q'): qs = qs.filter(Q(description__icontains=data['q'])|Q(category__icontains=data['q']))
    return qs

@login_required
def tx_list(request):
    form = FilterForm(request.GET or None)
    items = _apply_filters(Transaction.objects.all(), form.data if form.is_bound else {})
    totals = {
        'total': items.aggregate(s=Sum('amount'))['s'] or 0,
        'in': items.filter(kind='IN').aggregate(s=Sum('amount'))['s'] or 0,
        'out': items.filter(kind='OUT').aggregate(s=Sum('amount'))['s'] or 0,
    }
    return render(request,'finance/list.html',{'items':items,'form':form,'totals':totals})

@login_required
def tx_create(request):
    form = TxForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save(); messages.success(request,'Lançamento salvo.'); return redirect('finance:list')
    return render(request,'finance/form.html',{'form':form, 'is_edit': False})

@login_required
def tx_edit(request, pk):
    obj = get_object_or_404(Transaction, pk=pk)
    form = TxForm(request.POST or None, instance=obj)
    if request.method=='POST' and form.is_valid():
        form.save(); messages.success(request,'Lançamento atualizado.'); return redirect('finance:list')
    return render(request,'finance/form.html',{'form':form, 'is_edit': True})

@login_required
def tx_delete(request, pk):
    obj = get_object_or_404(Transaction, pk=pk)
    if request.method=='POST':
        obj.delete(); messages.success(request,'Lançamento removido.'); return redirect('finance:list')
    return render(request,'finance/confirm_delete.html',{'obj':obj})

@login_required
def recibo_pdf(request, pk):
    tx = get_object_or_404(Transaction, pk=pk)
    company = Company.objects.first()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=40,bottomMargin=40)
    elems = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleC', alignment=TA_CENTER, fontSize=16, spaceAfter=12))
    styles.add(ParagraphStyle(name='Just', alignment=TA_JUSTIFY, leading=16, fontSize=12))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=12, spaceBefore=20))

    if company and company.logo:
        try:
            img = Image(company.logo.path, width=120, height=120, kind='proportional')
            img.hAlign='CENTER'; elems.append(img); elems.append(Spacer(1,8))
        except Exception:
            pass

    elems.append(Paragraph('<b>RECIBO</b>', styles['TitleC']))
    importe = f"R$ {tx.amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    corpo = (f"Eu, <b>{company.name if company else '________'}</b>"
             + (f" (Doc.: {company.document})" if company and company.document else "")
             + f", declaro que recebi na data de {tx.date.strftime('%d/%m/%Y')} a importância de {importe} "
               f"referente a <i>{tx.description or '---'}</i>.")
    elems.append(Paragraph(corpo, styles['Just']))
    elems.append(Spacer(1, 60))
    elems.append(Paragraph('__________________________________________', styles['Center']))
    elems.append(Paragraph(company.name if company else 'Assinatura', styles['Center']))
    doc.build(elems)
    pdf = buffer.getvalue(); buffer.close()
    resp = HttpResponse(pdf, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename=recibo_{tx.pk}.pdf'
    return resp

@login_required
def relatorio_pdf(request):
    form = FilterForm(request.GET or None)
    items = _apply_filters(Transaction.objects.all(), form.data if form.is_bound else {})
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20,leftMargin=20, topMargin=30,bottomMargin=30)
    elems=[]

    styles=getSampleStyleSheet()
    elems.append(Paragraph('Relatório Financeiro', styles['Title']))
    data=[['Data','Tipo','Categoria','Descrição','Valor']]
    for t in items:
        data.append([t.date.strftime('%d/%m/%Y'), t.get_kind_display(), t.category, t.description, f"R$ {t.amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')])
    table=Table(data, hAlign='LEFT', colWidths=[60,60,100,220,70])
    table.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25, colors.grey),('BACKGROUND',(0,0),(-1,0), colors.lightgrey),('ALIGN',(-1,1),(-1,-1),'RIGHT')]))
    elems.append(table)
    elems.append(Spacer(1,10))
    total=items.aggregate(s=Sum('amount'))['s'] or 0
    ent=items.filter(kind='IN').aggregate(s=Sum('amount'))['s'] or 0
    sai=items.filter(kind='OUT').aggregate(s=Sum('amount'))['s'] or 0
    elems.append(Paragraph(f"Entradas: R$ {ent:,.2f}".replace(',', 'X').replace('.', ',').replace('X','.'), styles['Normal']))
    elems.append(Paragraph(f"Saídas: R$ {sai:,.2f}".replace(',', 'X').replace('.', ',').replace('X','.'), styles['Normal']))
    elems.append(Paragraph(f"Total: R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X','.'), styles['Normal']))
    doc.build(elems)
    pdf=buffer.getvalue(); buffer.close()
    resp=HttpResponse(pdf, content_type='application/pdf')
    resp['Content-Disposition']='attachment; filename=relatorio.pdf'
    return resp
