from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from apps.finance.models import Transaction
from apps.finance.views import FilterForm, _apply_filters

@login_required
def index(request):
    form = FilterForm(request.GET or None)
    qs = _apply_filters(Transaction.objects.all(), form.data if form.is_bound else {})
    income = qs.filter(kind='IN').aggregate(total=Sum('amount'))['total'] or 0
    expense = qs.filter(kind='OUT').aggregate(total=Sum('amount'))['total'] or 0
    balance = income - expense
    return render(request, 'dashboard/index.html', {'income':income,'expense':expense,'balance':balance,'form':form})
