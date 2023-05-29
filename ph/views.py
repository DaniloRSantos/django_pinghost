from django.shortcuts import render
from ph.models import EnderecoBusca, Hosts
import socket
from django.utils import timezone

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

        # Obter os dados enviados pelo formulário para o endereço
        cep = request.POST['cep']
        logradouro = request.POST['logradouro']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']

        # Criar um novo objeto EnderecoBusca com os dados fornecidos
        novo_endereco = EnderecoBusca.objects.create(
            cep=cep,
            logradouro=logradouro,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
        )

        # Associar o endereço criado ao host
        novo_host.endereco = novo_endereco
        novo_host.save()

        # Redirecionar para a página de sucesso ou fazer o processamento necessário

    context = {}
    return render(request, 'ph\cadastro_host.html', context)
