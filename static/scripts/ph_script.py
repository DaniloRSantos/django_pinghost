import csv
import subprocess
import datetime

def check_host_availability(ip_address):
    command = ['ping', '-n', '1', ip_address]
    ping_results = subprocess.run(command, capture_output=True, text=True)
    return ping_results.returncode == 0, ping_results.stdout

# Nome do arquivo CSV
nome_arquivo = 'static\data\enderecos.csv'

# Ler os dados do arquivo CSV existente
dados = []
with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_csv:
    leitor_csv = csv.reader(arquivo_csv)
    cabecalho = next(leitor_csv)  # Ler o cabeçalho
    dados = list(leitor_csv)  # Ler os dados restantes

# Iterar pelos dados e atualizar as colunas desejadas
for linha in dados:
    endereco_ip = linha[0]  # Obter o endereço IP da coluna desejada

    # Verificar a disponibilidade do host usando a função check_host_availability
    host_disponivel, ping_output = check_host_availability(endereco_ip)

    if host_disponivel:
        # Se o ping for bem-sucedido, atualizar "ok" na coluna desejada
        linha[5] = "ok"
        linha[6] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        # Se o ping falhar, atualizar a mensagem de erro na coluna desejada
        linha[5] = "Ping falhou"
        linha[6] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Salvar os dados atualizados no arquivo existente
with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv_atualizado:
    escritor_csv = csv.writer(arquivo_csv_atualizado)
    escritor_csv.writerow(cabecalho)  # Escrever o cabeçalho
    escritor_csv.writerows(dados)  # Escrever os dados atualizados

# Exibir as informações atualizadas linha a linha
for linha in dados:
    print(linha)
