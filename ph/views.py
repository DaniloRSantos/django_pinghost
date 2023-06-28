from django.shortcuts import render
from ph.models import EnderecoBusca, Hosts
import socket
from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib import messages
import logging


logger = logging.getLogger(__name__)

# Função para verificar a disponibilidade do host

def check_availability(ip_address):
    try:
        socket.create_connection((ip_address, 80), timeout=1)
        return True
    except Exception:
        return False

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
    }

    return render(request, 'ph\index.html', context)

def cadastrar_host(request):
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
        
        novo_host.save()
        id_novo_host = novo_host.id

        # Obter os dados enviados pelo formulário para o endereço
        cep = request.POST['cep']
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']

        host = Hosts.objects.get(id=id_novo_host)

        # Criar um novo objeto EnderecoBusca com os dados fornecidos
        novo_endereco = EnderecoBusca.objects.create(
            cep=cep,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            host_id=id_novo_host
        )

        # Associar o endereço criado ao host
        novo_host.endereco = novo_endereco

        #Exibir mensagem de sucesso
        messages.success(request, 'Host cadastrado com sucesso!')

        # Redirecionar para a página de sucesso ou fazer o processamento necessário

    context = {}
    return render(request, 'ph\cadastro_host.html', context)
    

def excluir_hosts(request):
    logger.info("Função Excluir")
    if request.method == 'POST':        
        # Obter os IDs dos hosts selecionados para exclusão
        host_ids = request.POST.getlist('host_checkbox')  # Lista de IDs dos hosts selecionados
        print("IDs dos hosts selecionados:", host_ids)

        for host_id in host_ids:
            logger.info("Dentro do For")
            host = Hosts.objects.get(id=host_id)

        hosts_selecionados = Hosts.objects.filter(id__in=host_ids)
        for host in hosts_selecionados:
            logger.info(f"Host selecionados: {host.nome_host}, IP: {host.ip_host}, DNS: {host.dns_host}")

            
        # Verificar se foram selecionados hosts para exclusão
        if host_ids:
            # Excluir os hosts correspondentes aos IDs selecionados
            hosts_excluidos = Hosts.objects.filter(id__in=host_ids).delete()

            # Obter o contador de hosts excluídos do dicionário
            contador_hosts_excluidos = hosts_excluidos[0]
            # Exibir mensagem de sucesso com o número de hosts excluídos
            messages.success(request, f'{contador_hosts_excluidos} hosts excluídos com sucesso!')

        # Redirecionar de volta para a página de hosts
        return redirect('index')
    else:
        messages.error(request, 'Falha ao excluir, Por favor tente novamente.')
        # Redirecionar de volta para a página de hosts
        return redirect('index')
