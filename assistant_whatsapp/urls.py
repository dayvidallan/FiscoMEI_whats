
from django.urls import path
from .views import webhook_verify, webhook_receive

app_name = "assistant_whatsapp"

urlpatterns = [
    path("webhooks/whatsapp", webhook_verify, name="verify"),
    path("webhooks/whatsapp/", webhook_receive, name="receive"),
]
