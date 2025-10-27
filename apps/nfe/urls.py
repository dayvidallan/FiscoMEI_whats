
from django.urls import path
from . import views
app_name='nfe'
urlpatterns=[path('', views.index, name='index')]
