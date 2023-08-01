import socket
import os
import requests
from django.shortcuts import redirect
import logging
from django.contrib import messages
from django.utils import timezone
from ph.models import Hosts, Eventos
from django.http import JsonResponse,HttpResponse, HttpResponseBadRequest
from dotenv import load_dotenv
from django.core.mail import send_mail
from django.conf import settings

load_dotenv()
api_key = os.getenv('API_KEY')
logger = logging.getLogger(__name__)

def carrega_host(request):
    hosts = Hosts.objects.all()
    
    # Obter todos os objetos de Hosts novamente após as atualizações
    hosts = Hosts.objects.all().values('id', 'status_host')
    return JsonResponse({'hosts': list(hosts)})


def atualizar_host(request):
    if request.method == 'POST':
        host_id = request.POST.get('host_id')
        host = Hosts.objects.get(id=host_id)
        host.ip_host = request.POST.get('ip_host')
        host.dns_host = request.POST.get('dns_host')
        host.nome_host = request.POST.get('nome_host')
        host.categoria_host = request.POST.get('categoria_host')
        test = check_availability(host.ip_host)
        host.status_host = test[0]
        host.save()

        endereco = host.enderecos.first() 
        endereco.cep = request.POST.get('cep')
        endereco.logradouro = request.POST.get('logradouro')
        endereco.numero = request.POST.get('numero')
        endereco.complemento = request.POST.get('complemento')
        endereco.bairro = request.POST.get('bairro')
        endereco.cidade = request.POST.get('cidade')
        endereco.estado = request.POST.get('estado')
        endereco.latitude = request.POST.get('latitude')
        endereco.longitude = request.POST.get('longitude')
        endereco.save()
        return HttpResponse(status=204)

    return HttpResponseBadRequest()



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

def check_availability(ip_address):
    try:
        socket.create_connection((ip_address, 80), timeout=1)
        return True, None
    except Exception as e:
        return False, str(e)
    
def envia_email(assunto, conteudo):
    send_mail(assunto, conteudo, settings.EMAIL_HOST_USER, [settings.DEFAUT_FROM_EMAIL])
    
#Tarefas agendadas:
def atualiza_host_sched():
    hosts = Hosts.objects.all()
    def update():
        host.time_host = timezone.now()
        host.status_host = result_ping
        host.save()
        evento = Eventos(host=host, success=result_ping, error_message=error_message)
        evento.save()
    
    def calc_temp():
        intervalo_tempo = timezone.now() - host.time_host
        dia = str(intervalo_tempo.days)
        horas = str(intervalo_tempo.seconds // 3600)
        minutos = str((intervalo_tempo.seconds // 60) % 60)
        return (dia, horas, minutos)
    # Iterar pelos objetos de Hosts e atualizar as colunas desejadas
    for host in hosts:
        
        result_ping, error_message = check_availability(host.ip_host)



        if host.status_host == 1 and result_ping == 0 :            
            print( "Queda host: " + host.nome_host )
            update()
            envia_email('Queda host '+ host.nome_host ,' O host de IP '+ host.ip_host + ' está sem comunicação.' + '\nHorário da queda: ' + str(host.time_host)[:-6] )

            
        elif host.status_host == 0 and result_ping == 1 :
            print("Retomada da comunicação: " + host.nome_host)
            dia, horas, minutos = calc_temp()
            print("comunicação restabelecida após " + dia + " dias, "+ horas + " horas e " + minutos+ " minutos sem comunicação.")
            update()

            
        else:
            if host.status_host == 0 and result_ping == 0:
                dia, horas, minutos = calc_temp()                
                print("sem comunicação ha " + dia + " dias, "+ horas + " horas e " + minutos+ " minutos.")     