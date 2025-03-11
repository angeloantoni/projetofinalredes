import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


import socket
import json
import psutil
from comum import config
from comum import utils
from comum.classes import DadosComputador

def get_system_info():
    cpu_count = psutil.cpu_count()
    mem_livre = utils.bytes_para_gb(psutil.virtual_memory().available)
    disco_livre = utils.bytes_para_gb(psutil.disk_usage('/').free)
    temp_cpu = -1  # Valor padrão para temperatura

    try:
        temp_cpu = psutil.sensors_temperatures()['coretemp'][0].current
    except Exception as e:
        print(f"Erro ao obter a temperatura da CPU: {e}")
        # Não levantamos a exceção, apenas imprimimos o erro e usamos o valor padrão

    return DadosComputador(cpu_count, mem_livre, disco_livre, temp_cpu)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        dados = get_system_info()
        dados_dict = dados.to_dict()
        dados_json = json.dumps(dados_dict)
        mensagem_criptografada = utils.criptografar(dados_json, config.CHAVE_CRIPTOGRAFIA)

        BROADCAST_ADDRESS = '10.25.255.255'  
        client_socket.sendto(mensagem_criptografada, (BROADCAST_ADDRESS, config.SERVER_PORT))

        print("Dados enviados via broadcast.")

    except Exception as e:
        print(f"Erro no cliente: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
