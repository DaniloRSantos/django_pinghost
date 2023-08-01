import os
import logging
from django.shortcuts import render
from ph.models import  Hosts,EnderecoBusca
from ph.tasks import check_availability
from dotenv import load_dotenv
from django.utils import timezone
from django.contrib import messages

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

def cadastrar_host(request):
    
    logger.info(f'Received POST request: {request.POST}')

    if request.method == 'POST':
        # Obter os dados enviados pelo formulário para o host
        ip_host = request.POST['ip_host']
        dns_host = request.POST['dns_host']
        nome_host = request.POST['nome_host']
        categoria_host = request.POST['categoria_host']
        test = check_availability(ip_host)
        status_host = test[0]
        # Criar um novo objeto Hosts com os dados fornecidos
        novo_host = Hosts.objects.create(
            ip_host=ip_host,
            dns_host=dns_host,
            nome_host=nome_host,
            categoria_host=categoria_host,
            time_host=timezone.now(),
            status_host= status_host,
        )
        
        # Obter os dados enviados pelo formulário para o endereço
        cep = request.POST['cep']
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

  

        # Criar um novo objeto EnderecoBusca com os dados fornecidos
        novo_endereco = EnderecoBusca.objects.create(
            cep=cep,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            latitude=latitude,
            longitude=longitude,
            host_id=novo_host

        )


        # Associar o endereço criado ao host
        novo_host.enderecos.add(novo_endereco)
        
        #Exibir mensagem de sucesso
        messages.success(request, 'Host cadastrado com sucesso!')

        # Redirecionar para a página de sucesso ou fazer o processamento necessário

    context = {
        'api_key': api_key
    }
    return render(request, 'ph/cadastro_host.html', context)


def editar_host(request):
    host_id = request.POST.get('host_id')
    host = Hosts.objects.get(id=host_id)
    endereco = host.enderecos.first()  # Obtém o primeiro EnderecoBusca relacionado ao host

    context = {
        'host' : host,
        'endereco': endereco,
    }
    return render(request, 'ph/editar_hosts.html',context)


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
