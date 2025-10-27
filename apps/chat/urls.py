
from django.urls import path
from . import views
app_name='chat'
urlpatterns=[
    path('', views.index, name='index'),
    path('api/messages/', views.messages_api, name='messages_api'),
]
