
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial = True
    dependencies = [('auth','0012_alter_user_first_name_max_length')]
    operations = [
        migrations.CreateModel(
            name='ChatThread',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('created_at', models.DateTimeField(auto_now_add=True)),
                    ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_threads', to='auth.user'))],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('role', models.CharField(choices=[('user','Usuário'),('bot','Assistente')], max_length=10)),
                    ('content', models.TextField()),
                    ('created_at', models.DateTimeField(auto_now_add=True)),
                    ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chatthread'))],
            options={'ordering':['id']},
        ),
    ]
