from django.urls import path
from . import views

app_name = 'das_mei'
urlpatterns = [
    path('', views.das_mei_home, name='home'),
    path('gerar/', views.gerar_das, name='gerar_das'),
]
