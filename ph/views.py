import os
import logging
from django.shortcuts import render
from ph.models import  Hosts
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('API_KEY')
logger = logging.getLogger(__name__)

def index(request):
    # Obter todos os objetos de Hosts
    hosts = Hosts.objects.all()

    context = {
        'hosts': hosts,
        'imagem_inicial': 'loading.gif',
        'api_key': api_key,  
    }

    return render(request, 'ph/index.html', context)

def mapa(request):
    hosts = Hosts.objects.all()
    host_data = []
    for host in hosts:
        endereco = host.enderecos.first()  # Acessa o primeiro objeto EnderecoBusca associado ao host (ou None)

        if endereco:
            latitude = float(endereco.latitude)
            longitude = float(endereco.longitude)
            host.coordenadas = (latitude, longitude)
            host.save()

            host_data.append({
                'latitude': latitude,
                'longitude': longitude,
                'nome_host': host.nome_host,
                'status_host': host.status_host,
            })

    context = {
        'host_data': host_data
    }

    logger.info('Retorno de coordenadas: %s', host_data)

    return render(request, 'ph/mapa.html', {'host_data':host_data})
