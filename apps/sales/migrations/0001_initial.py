
from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=120)),
                ('product_name', models.CharField(max_length=120)),
                ('value', models.DecimalField(decimal_places=2, max_digits=12, default=Decimal('0.00'))),
                ('date', models.DateField()),
                ('receipt_pdf', models.FileField(blank=True, null=True, upload_to='receipts/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering':['-date','-id']},
        ),
    ]
