import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


import socket
import json
from comum import config
from comum import utils

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', config.SERVER_PORT))

    print(f"Servidor UDP ouvindo na porta {config.SERVER_PORT}...")

    try:
        while True:
            message, address = server_socket.recvfrom(4096)
            try:
                mensagem_descriptografada = utils.descriptografar(message, config.CHAVE_CRIPTOGRAFIA)
                data = json.loads(mensagem_descriptografada)

                # Formatação da saída
                print(f"Dados recebidos de: {address[0]}")  # Apenas o endereço IP
                print(f"  CPU Cores: {data['cpu_count']}")
                print(f"  Memória Livre: {data['mem_livre']} GB")
                print(f"  Disco Livre: {data['disco_livre']} GB")
                print(f"  Temperatura CPU: {data['temp_cpu']} °C")
                print("-" * 20)  # Separador

            except Exception as e:
                print(f"Erro ao descriptografar/decodificar a mensagem de {address}: {e}")

    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()