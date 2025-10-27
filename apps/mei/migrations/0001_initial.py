
from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='MEI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_name', models.CharField(max_length=120, verbose_name='Nome do titular')),
                ('cpf', models.CharField(blank=True, max_length=14, verbose_name='CPF')),
                ('cnpj', models.CharField(max_length=18, unique=True, verbose_name='CNPJ')),
                ('trade_name', models.CharField(blank=True, max_length=120, verbose_name='Nome fantasia')),
                ('corporate_name', models.CharField(blank=True, max_length=180, verbose_name='Razão social')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='Endereço')),
                ('city', models.CharField(blank=True, max_length=80, verbose_name='Cidade')),
                ('state', models.CharField(blank=True, max_length=2, verbose_name='UF')),
                ('cep', models.CharField(blank=True, max_length=9, verbose_name='CEP')),
                ('im', models.CharField(blank=True, max_length=40, verbose_name='Inscrição Municipal')),
                ('ie', models.CharField(blank=True, max_length=40, verbose_name='Inscrição Estadual')),
                ('regime', models.CharField(default='SIMEI', max_length=50, verbose_name='Regime Tributário')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name':'MEI','verbose_name_plural':'MEIs'},
        ),
    ]
