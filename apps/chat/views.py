
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from .models import ChatThread, ChatMessage

def _get_or_create_thread(user):
    thread = ChatThread.objects.filter(user=user).first()
    if not thread:
        thread = ChatThread.objects.create(user=user)
        ChatMessage.objects.create(thread=thread, role='bot',
            content='Oi! Sou o assistente do FiscoMEI. Posso ajudar com MEI, lançamentos e dúvidas rápidas.')
    return thread

def _bot_reply(text:str)->str:
    t = text.strip().lower()
    if any(k in t for k in ['saldo','balance']):
        return 'Para ver o saldo, acesse o Dashboard. Em breve mostro aqui também.'
    if 'cadastrar mei' in t or 'novo mei' in t:
        return 'Use MEIs → "Novo MEI". Em breve abrirei o formulário direto pelo chat.'
    if any(k in t for k in ['lançar','lancamento','entrada','saída','saida']):
        return 'Para lançar: Finanças → "Novo lançamento". Em breve lanço por aqui.'
    return 'Entendi. Em breve terei ações diretas (abrir telas, lançar valores). O que mais precisa?'

@login_required
def index(request):
    thread = _get_or_create_thread(request.user)
    get_token(request)  # seta cookie CSRF
    return render(request,'chat/index.html',{'thread':thread})

@login_required
@require_http_methods(['GET','POST'])
def messages_api(request):
    thread = _get_or_create_thread(request.user)
    if request.method=='GET':
        after = request.GET.get('after')
        qs = thread.messages.all()
        if after and after.isdigit(): qs = qs.filter(id__gt=int(after))
        data = [{'id':m.id,'role':m.role,'content':m.content,'created_at':m.created_at.isoformat()} for m in qs]
        return JsonResponse({'messages':data})
    content = (request.POST.get('content') or '').strip()
    if not content: return HttpResponseBadRequest('content required')
    user_msg = ChatMessage.objects.create(thread=thread, role='user', content=content)
    bot_msg = ChatMessage.objects.create(thread=thread, role='bot', content=_bot_reply(content))
    return JsonResponse({'ok':True,'user_id':user_msg.id,'bot_id':bot_msg.id})
