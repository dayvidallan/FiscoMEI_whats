from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# URL do portal PGMEI para consulta e geração de DAS
PGMEI_URL = "https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao"

@login_required
def das_mei_home(request):
    """
    Exibe a página inicial da funcionalidade DAS MEI.
    Consulta a DAS em aberto e exibe a mensagem de confirmação.
    """
    # Lógica simplificada para simular a consulta da DAS em aberto.
    # Em um ambiente real, seria necessário um processo de web scraping ou integração
    # mais robusta com o portal da Receita Federal, o que é complexo e não seguro
    # para ser feito diretamente aqui sem credenciais e tratamento de captcha.

    # Simulação: A DAS em aberto é sempre a do mês anterior ao atual.
    today = datetime.now()
    mes_referencia_dt = today.replace(day=1) # Começa no dia 1
    # Se for o dia 1, a DAS em aberto é a de 2 meses atrás (ex: jan/2026, DAS dez/2025)
    # Se for depois do dia 1, a DAS em aberto é a do mês anterior (ex: 2/jan/2026, DAS dez/2025)
    # A DAS vence no dia 20 do mês subsequente ao de referência.
    # Vamos considerar que a DAS em aberto é a do mês anterior.
    if today.day > 20:
        # Se for depois do dia 20, a DAS do mês anterior já venceu e está em aberto.
        # A próxima DAS a vencer é a do mês atual.
        # Mas o usuário quer saber a DAS em aberto, que é a vencida.
        # A DAS de Outubro (referência) vence em Novembro.
        # Se estamos em Outubro, a DAS em aberto é a de Setembro (vencida em Outubro).
        if mes_referencia_dt.month == 1:
            mes_referencia_dt = mes_referencia_dt.replace(year=mes_referencia_dt.year - 1, month=12)
        else:
            mes_referencia_dt = mes_referencia_dt.replace(month=mes_referencia_dt.month - 1)
    else:
        # Se for antes do dia 20, a DAS do mês anterior ainda está para vencer ou venceu recentemente.
        # A DAS em aberto é a do mês anterior.
        if mes_referencia_dt.month == 1:
            mes_referencia_dt = mes_referencia_dt.replace(year=mes_referencia_dt.year - 1, month=12)
        else:
            mes_referencia_dt = mes_referencia_dt.replace(month=mes_referencia_dt.month - 1)

    mes_referencia = mes_referencia_dt.strftime("%B").capitalize()
    ano_referencia = mes_referencia_dt.year

    context = {
        'mes_referencia': mes_referencia,
        'ano_referencia': ano_referencia,
    }
    return render(request, 'das_mei/home.html', context)

@login_required
def gerar_das(request):
    """
    Simula a geração da DAS e retorna um link.
    """
    if request.method == 'POST':
        # Lógica para simular a geração da DAS.
        # Em um ambiente real, este seria o ponto onde a automação do navegador
        # (ex: Selenium/Playwright) seria usada para interagir com o portal da Receita Federal.
        # Devido à complexidade e restrições de segurança (CAPTCHA, credenciais),
        # estamos simulando a geração.

        # Simulação: Retorna um link para o portal PGMEI (como solicitado, um link)
        link_das = PGMEI_URL

        return JsonResponse({
            'success': True,
            'message': f'DAS do mês de {request.POST.get("mes_referencia")} de {request.POST.get("ano_referencia")} gerada com sucesso!',
            'link_das': link_das
        })
    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)
