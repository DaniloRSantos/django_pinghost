from django.urls import path
from ph import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastrar_host, name='cadastrar_host'),
    path('carregar_coordenadas/', views.carregar_coordenadas, name='carregar_coordenadas'),
    path('excluir/', views.excluir_hosts, name='excluir_hosts'),
    path('api-key/', views.get_api_key, name='api_key'),
    path('mapa/', views.mapa, name='mapa'),

]