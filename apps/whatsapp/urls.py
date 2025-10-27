from django.urls import path
from . import views

urlpatterns = [
    path("", views.verify, name="wa_verify"),
    path("", views.receive, name="wa_receive"),
]