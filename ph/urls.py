from django.urls import path
from ph import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastrar_host, name='cadastrar_host'),
    path('excluir/', views.excluir_hosts, name='excluir_hosts'),
]