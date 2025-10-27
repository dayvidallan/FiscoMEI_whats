
from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('IN','Entrada'),('OUT','Saída')], default='IN', max_length=3)),
                ('date', models.DateField()),
                ('category', models.CharField(blank=True, max_length=80)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering':['-date','-id']},
        ),
    ]
