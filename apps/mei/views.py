
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import ModelForm
from .models import MEI
class MEIForm(ModelForm):
    class Meta:
        model = MEI
        fields = ['owner_name','cpf','cnpj','trade_name','corporate_name','email','phone','address','city','state','cep','im','ie','regime']
@login_required
def mei_list(request):
    items = MEI.objects.order_by('-created_at')
    return render(request, 'mei/list.html', {'items': items})
@login_required
def mei_create(request):
    form = MEIForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        obj = form.save(); messages.success(request,'MEI cadastrado.'); return redirect('mei:detail', pk=obj.pk)
    return render(request,'mei/form.html',{'form':form})
@login_required
def mei_update(request, pk):
    obj = get_object_or_404(MEI, pk=pk)
    form = MEIForm(request.POST or None, instance=obj)
    if request.method=='POST' and form.is_valid():
        form.save(); messages.success(request,'MEI atualizado.'); return redirect('mei:detail', pk=pk)
    return render(request,'mei/form.html',{'form':form})
@login_required
def mei_detail(request, pk):
    obj = get_object_or_404(MEI, pk=pk)
    return render(request,'mei/detail.html',{'obj':obj})
