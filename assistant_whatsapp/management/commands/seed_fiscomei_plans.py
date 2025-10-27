
from django.core.management.base import BaseCommand
from assistant_whatsapp.services import get_or_seed_plans

class Command(BaseCommand):
    help = "Cria/atualiza os planos padrão do FiscoMEI"

    def handle(self, *args, **kwargs):
        ps = get_or_seed_plans()
        self.stdout.write(self.style.SUCCESS(f"{len(ps)} planos verificados/criados."))
