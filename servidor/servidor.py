import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


import socket
import threading
import json
from comum import config
from comum import utils
from comum.classes import DadosComputador

# Dicionário para armazenar informações dos clientes conectados
clientes = {}  # { (ip, porta): DadosComputador }
lock = threading.Lock() # Para evitar race conditions ao acessar 'clientes'

def handle_client(client_socket, client_address):
    """Lida com a conexão de um cliente."""
    try:
        mensagem_criptografada = client_socket.recv(1024)
        mensagem_json = utils.descriptografar(mensagem_criptografada, config.CHAVE_CRIPTOGRAFIA)
        dados_dict = json.loads(mensagem_json)  #Converte JSON de volta para dicionário
        dados = DadosComputador(**dados_dict)

        with lock:
            clientes[client_address] = dados  # Armazena os dados do cliente

        print(f"Dados recebidos de {client_address}: CPU: {dados.cpu_count}, Mem Livre: {dados.mem_livre:.2f} GB, Disco Livre: {dados.disco_livre:.2f} GB, Temp CPU: {dados.temp_cpu}")

        # Cálculo da média
        if dados.temp_cpu > 0:
            media = (dados.cpu_count + dados.mem_livre + dados.disco_livre + dados.temp_cpu) / 4
        else:
            media = (dados.cpu_count + dados.mem_livre + dados.disco_livre) / 3 # Calcula a média sem a temperatura

        resposta = f"Média dos dados: {media}"
        resposta_criptografada = utils.criptografar(resposta, config.CHAVE_CRIPTOGRAFIA)
        client_socket.send(resposta_criptografada)

    except Exception as e:
        print(f"Erro ao lidar com o cliente {client_address}: {e}")
    finally:
        with lock:
            if client_address in clientes:
                del clientes[client_address]  # Remove o cliente ao desconectar
        client_socket.close()

def main():
    """Função principal do servidor."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', config.SERVER_PORT))  # Ouve em todas as interfaces
    server_socket.listen(5)  # Permite até 5 conexões pendentes

    print(f"Servidor ouvindo na porta {config.SERVER_PORT}...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Conexão recebida de {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except Exception as e:
        print(f"Erro no loop principal do servidor: {e}")
    finally:
        server_socket.close()
        print("Servidor fechado.")


if __name__ == "__main__":
    main()