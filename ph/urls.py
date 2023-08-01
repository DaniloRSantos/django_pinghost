from django.urls import path
from ph import views,tasks
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),    
    path('mapa/', views.mapa, name='mapa'),
    path('cadastro/', views.cadastrar_host, name='cadastrar_host'),
    path('carregar_coordenadas/', tasks.carregar_coordenadas, name='carregar_coordenadas'),
    path('excluir/', tasks.excluir_hosts, name='excluir_hosts'),
    path('api-key/', tasks.get_api_key, name='api_key'),
    path('carrega_host/', tasks.carrega_host, name='carrega_host'),    
    path('editar_host/', views.editar_host, name='retorna_host'),
    path('atualizar_host/', tasks.atualizar_host, name='atualizar_host'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

