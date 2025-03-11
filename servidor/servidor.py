import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


import socket
import json
from comum import config
from comum import utils
import threading

dados_clientes = {}  
lock = threading.Lock()  

def calcular_media_cliente(ip_cliente):
    """Calcula a média dos dados para um cliente específico."""
    with lock:
        if ip_cliente not in dados_clientes or not dados_clientes[ip_cliente]:
            return "Nenhum dado recebido para este cliente ainda."

        total_cpu = 0
        total_mem = 0
        total_disco = 0
        total_temp = 0
        num_leituras = len(dados_clientes[ip_cliente])

        for leitura in dados_clientes[ip_cliente]:
            total_cpu += leitura['cpu_count']
            total_mem += leitura['mem_livre']
            total_disco += leitura['disco_livre']
            total_temp += leitura['temp_cpu']

        media_cpu = total_cpu / num_leituras
        media_mem = total_mem / num_leituras
        media_disco = total_disco / num_leituras
        media_temp = total_temp / num_leituras

        return (
            f"Média para {ip_cliente}:\n"
            f"  CPU Cores: {media_cpu:.2f}\n"
            f"  Memória Livre: {media_mem:.2f} GB\n"
            f"  Disco Livre: {media_disco:.2f} GB\n"
            f"  Temperatura CPU: {media_temp:.2f} °C"
        )

def listar_computadores():
    """Lista os computadores que estão enviando dados."""
    with lock:
        if not dados_clientes:
            print("Nenhum computador enviando dados no momento.")
            return

        print("Computadores Ativos:")
        for i, ip in enumerate(dados_clientes.keys()):
            print(f"{i+1}. {ip}")

def detalhar_computador(ip_cliente):
    """Exibe os detalhes de um computador específico."""
    with lock:
        if ip_cliente not in dados_clientes:
            print(f"Nenhum dado recebido para o computador {ip_cliente}.")
            return

        print(f"Detalhes do computador {ip_cliente}:")
        print("-" * 20)

        # Exibe os dados mais recentes
        dados_recentes = dados_clientes[ip_cliente][-1] # Pega a última leitura
        print("Dados mais recentes:")
        print(f"  CPU Cores: {dados_recentes['cpu_count']}")
        print(f"  Memória Livre: {dados_recentes['mem_livre']} GB")
        print(f"  Disco Livre: {dados_recentes['disco_livre']} GB")
        print(f"  Temperatura CPU: {dados_recentes['temp_cpu']} °C")
        print("-" * 20)

        # Exibe a média
        media = calcular_media_cliente(ip_cliente)
        print(media)

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
                ip_cliente = address[0]

                with lock:
                    
                    if ip_cliente not in dados_clientes:
                        dados_clientes[ip_cliente] = []
                    dados_clientes[ip_cliente].append(data)

               
                print(f"Dados recebidos de: {ip_cliente}")
                print(f"  CPU Cores: {data['cpu_count']}")
                print(f"  Memória Livre: {data['mem_livre']} GB")
                print(f"  Disco Livre: {data['disco_livre']} GB")
                print(f"  Temperatura CPU: {data['temp_cpu']} °C")
                print("-" * 20)

                media_cliente = calcular_media_cliente(ip_cliente)  
                print(media_cliente) 
                print("-" * 20)

            except Exception as e:
                print(f"Erro ao descriptografar/decodificar a mensagem de {address}: {e}")


            # Menu Interativo
            print("\nOpções:")
            print("1. Listar computadores")
            print("2. Detalhar computador")
            print("3. Continuar ouvindo")
            print("Escolha uma opção (1, 2 ou 3):")
            opcao = input()

            if opcao == "1":
                listar_computadores()
            elif opcao == "2":
                listar_computadores()
                ip_escolhido = input("Digite o IP do computador que deseja detalhar: ")
                detalhar_computador(ip_escolhido)
            elif opcao == "3":
                pass  
            else:
                print("Opção inválida.")

    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()