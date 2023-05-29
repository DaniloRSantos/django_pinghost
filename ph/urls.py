from django.urls import path
from ph import views

urlpatterns = [
    path('', views.index),
    path('cadastro/', views.cadastrar_host, name='cadastrar_host'),
]