
# assistant_whatsapp (FiscoMEI)

Camada de WhatsApp + IA (GPT-4o-mini) integrada ao Django principal do FiscoMEI, com controle de planos e limites.

## Rotas
- Verificação webhook (GET): `/assistant-wa/webhooks/whatsapp`
- Recebimento webhook (POST): `/assistant-wa/webhooks/whatsapp/`

## Instalação
1. Adicione `'assistant_whatsapp'` ao `INSTALLED_APPS`.
2. Em `urls.py` principal:
   ```py
   path("assistant-wa/", include("assistant_whatsapp.urls"))
   ```
3. Variáveis de ambiente:
   ```
   WA_VERIFY_TOKEN=fiscoMEI_XHJD_2025
   WA_TOKEN=SEU_TOKEN_META
   WA_PHONE_NUMBER_ID=SEU_ID
   WA_API_VERSION=v21.0
   OPENAI_API_KEY=sk-...
   ASSISTANT_MODEL=gpt-4o-mini
   ```
4. Migrações:
   ```bash
   python manage.py migrate
   python manage.py seed_fiscomei_plans
   ```
5. Configure o webhook na Meta para:
   - Verify token: `WA_VERIFY_TOKEN`
   - URL de verificação (GET) e recebimento (POST):
     `https://SEU-DOMINIO/assistant-wa/webhooks/whatsapp`

## Integração com MEI/User
- O número do WhatsApp deve estar em `apps.mei.models.MEI.telefone` (ou ajuste em `services.find_user_by_phone`).

## Lançamentos Financeiros
- Por padrão tenta criar em `apps.finance.models.Entrada`/`Saida` (ajuste se seus modelos tiverem outros nomes/campos).
- Se não encontrar, cria no espelho `assistant_whatsapp.LancamentoEspelho` como fallback.

## Limites e Planos
- Planos padrão:
  - Básico: 200 mensagens/mês — R$ 49,90
  - Pro: 500 mensagens/mês — R$ 89,90
  - Ilimitado (Fair Use): 2.000 mensagens/mês — R$ 129,90
- Mensagens acima de 90% do limite recebem alerta;
- Ao estourar o limite, o usuário recebe um aviso de renovação e o bot não processa até liberar.

## Observações
- Se não definir `OPENAI_API_KEY`, o parser simples por regex entra em ação.
- Personalize mensagens em `views.py` e custos no painel admin.
