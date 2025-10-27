
from django.db import models
from django.contrib.auth.models import User
class ChatThread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_threads')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Thread {self.pk} - {self.user.username}'
class ChatMessage(models.Model):
    ROLE_CHOICES=[('user','Usuário'),('bot','Assistente')]
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['id']
    def __str__(self): return f'[{self.role}] {self.content[:30]}'
