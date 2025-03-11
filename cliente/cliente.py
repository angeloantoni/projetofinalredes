import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


import socket
import psutil
import json  # Para serializar dados para envio
from comum import config
from comum import utils
from comum.classes import DadosComputador

def get_system_info():
    """Coleta informações do sistema."""
    cpu_count = psutil.cpu_count()
    mem_livre = utils.bytes_para_gb(psutil.virtual_memory().available)  # Em bytes
    disco_livre = utils.bytes_para_gb(psutil.disk_usage('/').free)  # Em bytes
    try:
        temp_cpu = psutil.sensors_temperatures()['coretemp'][0].current  # Requer permissões
    except Exception as e:
        temp_cpu = -1 # ou algum valor padrão
        print(f"Erro ao obter a temperatura da CPU: {e}")

    return DadosComputador(cpu_count, mem_livre, disco_livre, temp_cpu)


def main():
    """Função principal do cliente."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(('localhost', config.SERVER_PORT)) #Conecta ao servidor

        dados = get_system_info()
        dados_json = json.dumps(dados.__dict__)
        mensagem_criptografada = utils.criptografar(dados_json, config.CHAVE_CRIPTOGRAFIA)
        client_socket.send(mensagem_criptografada)


        resposta_criptografada = client_socket.recv(1024)
        resposta = utils.descriptografar(resposta_criptografada, config.CHAVE_CRIPTOGRAFIA)
        print(f"Resposta do servidor: {resposta}")

    except ConnectionRefusedError:
        print("Servidor não encontrado. Certifique-se de que o servidor está rodando.")
    except Exception as e:
        print(f"Erro no cliente: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()