from django.urls import path
from . import views
app_name = 'finance'
urlpatterns = [
    path('', views.tx_list, name='list'),
    path('novo/', views.tx_create, name='create'),
    path('<int:pk>/editar/', views.tx_edit, name='edit'),
    path('<int:pk>/excluir/', views.tx_delete, name='delete'),
    path('<int:pk>/recibo/', views.recibo_pdf, name='recibo'),
    path('relatorio/pdf/', views.relatorio_pdf, name='relatorio_pdf'),
]
