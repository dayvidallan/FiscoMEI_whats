
from django.urls import path
from . import views
app_name = 'mei'
urlpatterns = [
    path('', views.mei_list, name='list'),
    path('novo/', views.mei_create, name='create'),
    path('<int:pk>/editar/', views.mei_update, name='update'),
    path('<int:pk>/', views.mei_detail, name='detail'),
]
