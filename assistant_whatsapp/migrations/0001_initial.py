
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30, unique=True)),
                ('limite_mensal', models.PositiveIntegerField(default=200)),
                ('preco', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('descricao', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MensagemLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(db_index=True, max_length=32)),
                ('tipo', models.CharField(default='text', max_length=20)),
                ('conteudo', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UsoMensal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(max_length=7)),
                ('mensagens', models.PositiveIntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plano', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assistant_whatsapp.plano')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usos_whatsapp', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'mes')},
            },
        ),
        migrations.CreateModel(
            name='LancamentoEspelho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('saida', 'Saída')], max_length=10)),
                ('valor_centavos', models.IntegerField()),
                ('descricao', models.TextField(blank=True)),
                ('data', models.DateField()),
                ('origem', models.CharField(blank=True, max_length=120)),
                ('cpf_cnpj', models.CharField(blank=True, max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
