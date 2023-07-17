import os
import socket
import logging
import requests
import json
import requests
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from ph.models import EnderecoBusca, Hosts
from django.http import JsonResponse
from dotenv import load_dotenv

from django.http import JsonResponse
from django.contrib import messages



logger = logging.getLogger(__name__)

# Função para verificar a disponibilidade do host

def check_availability(ip_address):
    try:
        socket.create_connection((ip_address, 80), timeout=1)
        return True
    except Exception:
        return False
    



load_dotenv()
api_key = os.getenv('API_KEY')


def carregar_coordenadas(request):
    if request.method == 'POST':
        cep = request.POST.get('cep')
        logradouro = request.POST.get('logradouro')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        endereco = f'{logradouro}, {numero}, {bairro}, {cidade}, {estado}, {cep}, {complemento}'
        endereco_codificado = endereco.replace(' ', '%20')
        api_key = os.getenv('API_KEY')

        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={endereco_codificado}&key={api_key}'

        print(f'Endereço enviado: {endereco}')

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK' and len(data['results']) > 0:
                    location = data['results'][0]['geometry']['location']
                    latitude = location['lat']
                    longitude = location['lng']
                    print(f'As coordenadas do endereço são: Latitude={latitude}, Longitude={longitude}')
                    return JsonResponse({'latitude': latitude, 'longitude': longitude})
                else:
                    print('Não foi possível obter as coordenadas do endereço.')
                    return JsonResponse({'error': 'Não foi possível obter as coordenadas do endereço.'}, status=400)
            else:
                print('A requisição falhou.')
                return JsonResponse({'error': 'A requisição falhou.'}, status=400)
        except requests.exceptions.RequestException as e:
            logger.error(f'Erro ao fazer a requisição: {e}')
            messages.error(request, 'Ocorreu um erro ao obter as coordenadas.')
            return JsonResponse({'error': 'Ocorreu um erro ao obter as coordenadas.'}, status=400)
        except KeyError as e:
            logger.error(f'Dados de resposta inválidos: {e}')
            messages.error(request, 'Ocorreu um erro ao processar os dados de resposta.')
            return JsonResponse({'error': 'Ocorreu um erro ao processar os dados de resposta.'}, status=400)
    else:
        return JsonResponse({'error': 'Método inválido'}, status=400)


def get_api_key(request):
    api_key = os.getenv('API_KEY')  # Obtenha a chave da API do ambiente
    return JsonResponse({'api_key': api_key})



def carrega_dados(request):
    # Obter todos os objetos de Hosts
    hosts = Hosts.objects.all()

    context = {
        'hosts': hosts,
        'imagem_inicial': 'loading.gif',
        'API_KEY': api_key,  # Adicione a API key ao dicionário de contexto
    }

    return render(request, 'ph/index.html', context)

def index(request):
    # Obter todos os objetos de Hosts
    hosts = Hosts.objects.all()

    # Iterar pelos objetos de Hosts e atualizar as colunas desejadas
    for host in hosts:
        endereco_ip = host.ip_host  # Obter o endereço IP do objeto Host

        # Verificar a disponibilidade do host usando a função check_availability
        host_disponivel = check_availability(endereco_ip)
        if host_disponivel:
            # Se o ping for bem-sucedido, atualizar o status do host para True
            host.status_host = True
            
        else:
            # Se o ping falhar, atualizar o status do host para False
            host.status_host = False
        
       
        host.time_host = timezone.now()
        host.save()  # Salvar as alterações no objeto Host

    # Obter todos os objetos de Hosts novamente após as atualizações
    hosts_atualizados = Hosts.objects.all()

    context = {
        'hosts': hosts_atualizados,
        'imagem_inicial': 'loading.gif',
        'api_key': api_key,  # Adicione a API key ao dicionário de contexto
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

        # Criar um novo objeto Hosts com os dados fornecidos
        novo_host = Hosts.objects.create(
            ip_host=ip_host,
            dns_host=dns_host,
            nome_host=nome_host,
            categoria_host=categoria_host,
            time_host=timezone.now(),
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
    
def excluir_hosts(request):
    if request.method == 'POST':
        host_ids = request.POST.get('host_ids')
        
        host_ids_list = [int(id) for id in host_ids.split(",")]

        logger.info(f'IDs dos hosts selecionados para exclusão: {host_ids_list}')
        
        try:
            # Excluindo os hosts com base nos IDs fornecidos
            hosts = Hosts.objects.filter(id__in=host_ids_list)
            hosts.delete()

            #messages.success(request, 'Hosts excluídos com sucesso.')
        except Exception as e:
            logger.error(f'Erro ao excluir hosts: {e}')
            messages.error(request, 'Ocorreu um erro ao excluir os hosts.')
            
    return redirect('index')





def mapa(request):
    hosts = Hosts.objects.all()
    host_data = []
    for host in hosts:
        endereco = host.enderecos.first()  # Acessa o primeiro objeto EnderecoBusca associado ao host (ou None)

        if endereco:

            host_data.append({
                'latitude': float(endereco.latitude),
                'longitude': float(endereco.longitude),
                'nome_host': host.nome_host,
            })

    context = {
        'host_data': host_data
    }

    logger.info('Retorno de coordenadas: %s', host_data)

    return render(request, 'ph/mapa.html', {'host_data':host_data})




#def editar_host(request, host_id):
#
#    host = get_object_or_404(Host, pk=host_id)
#
#    if request.method == 'POST':
#        if form.is_valid():
#            form.save()
#            return redirect('index')
#    else:
#        form = HostForm(instance=host)
#
#    return render(request, 'ph/editar_host.html', {'form': form, 'host': host})


#def obter_coordenadas(request):
#    endereco = request.GET.get('endereco')  # Obtém o endereço da query string
#    api_key = os.getenv('API_KEY')
#
#    url = 'https://maps.googleapis.com/maps/api/geocode/json'
#    params = {'address': endereco, 'key': api_key}
#    
#    response = requests.get(url, params=params)
#    data = response.json()
#
#    if data['status'] == 'OK':
#        result = data['results'][0]
#        location = result['geometry']['location']
#        latitude = location['lat']
#        longitude = location['lng']
#        response_data = {
#            'latitude': latitude,
#            'longitude': longitude
#        }
#        return JsonResponse(response_data)
#    else:
#        response_data = {
#            'error': 'Não foi possível obter as coordenadas.'
#        }
#        return JsonResponse(response_data, status=400)
#