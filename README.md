## Fluxo de Funcionamento da Aplicação de Monitoramento de Computadores

**1. Inicialização**

*   **Servidor:**
    1.  Execução do script `servidor/servidor.py`.
    2.  Criação de um socket TCP (protocolo de comunicação confiável):
        *   `server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
    3.  Associação do socket a um endereço IP e porta específicos:
        *   `server_socket.bind(('0.0.0.0', config.SERVER_PORT))`
        *   O servidor escuta em todas as interfaces de rede (0.0.0.0) na porta definida em `comum/config.py`.
    4.  Início da escuta por conexões de clientes:
        *   `server_socket.listen(5)`
        *   Permite até 5 conexões em espera.
    5.  Exibição de mensagem no console informando que o servidor está em execução.

*   **Cliente:**
    1.  Execução do script `cliente/cliente.py`.
    2.  Criação de um socket TCP:
        *   `client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
    3.  Tentativa de conexão ao servidor no endereço IP e porta definidos:
        *   `client_socket.connect(('localhost', config.SERVER_PORT))`
        *   O cliente tenta se conectar ao servidor rodando localmente (localhost) na porta definida em `comum/config.py`.

**2. Coleta de Dados no Cliente**

1.  Chamada da função `get_system_info()` para coletar dados do sistema.
2.  Utilização da biblioteca `psutil` para obter:
    *   Número de CPUs lógicas: `psutil.cpu_count()`
    *   Memória RAM disponível (livre) em bytes: `psutil.virtual_memory().available`
    *   Espaço livre no disco rígido (partição raiz) em bytes: `psutil.disk_usage('/').free`
    *   (Tentativa de obter) Temperatura atual do processador: `psutil.sensors_temperatures()['coretemp'][0].current` (pode requerer permissões)
3.  Conversão dos valores de memória e disco de bytes para Gigabytes (GB) usando `utils.bytes_para_gb()`.
4.  Criação de um objeto da classe `DadosComputador` com os dados coletados.

**3. Envio de Dados do Cliente para o Servidor**

1.  Conversão do objeto `DadosComputador` para uma string JSON:
    *   `dados_json = json.dumps(dados.__dict__)`
    *   Utiliza a biblioteca `json` para formatar os dados em um formato textual padrão.
2.  Criptografia da string JSON usando a função `utils.criptografar()` e a chave definida em `comum/config.py`:
    *   `mensagem_criptografada = utils.criptografar(dados_json, config.CHAVE_CRIPTOGRAFIA)`
    *   Garante a segurança da transmissão.
3.  Envio da mensagem criptografada para o servidor através do socket:
    *   `client_socket.send(mensagem_criptografada)`

**4. Recebimento e Processamento de Dados no Servidor**

1.  Aceitação da conexão do cliente:
    *   `client_socket, client_address = server_socket.accept()`
    *   Cria um novo socket para a comunicação com o cliente.
2.  Criação de uma nova thread para lidar com a comunicação com o cliente:
    *   `client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))`
    *   Permite que o servidor lide com múltiplos clientes simultaneamente.
3.  Execução da função `handle_client()` na nova thread.
4.  Recebimento da mensagem criptografada do cliente:
    *   `mensagem_criptografada = client_socket.recv(1024)`
    *   Recebe até 1024 bytes de dados.
5.  Descriptografia da mensagem usando a função `utils.descriptografar()` e a chave de criptografia:
    *   `mensagem_json = utils.descriptografar(mensagem_criptografada, config.CHAVE_CRIPTOGRAFIA)`
6.  Conversão da string JSON para um dicionário Python:
    *   `dados_dict = json.loads(mensagem_json)`
7.  Criação de um objeto `DadosComputador` a partir do dicionário.
8.  Exibição dos dados recebidos no console do servidor:
    *   `print(f"Dados recebidos de {client_address}: ...")`
9.  Cálculo da média dos dados (CPU, Memória, Disco, Temperatura).
10. Formatação de uma mensagem contendo a média.
11. Criptografia da mensagem contendo a média.
12. Envio da mensagem criptografada de volta para o cliente.

**5. Resposta do Servidor e Exibição no Cliente**

1.  O cliente recebe a mensagem criptografada do servidor.
2.  A mensagem é descriptografada.
3.  A mensagem (contendo a média) é exibida no console do cliente.

**6. Encerramento**

*   **Cliente:**
    1.  Fechamento da conexão com o servidor:
        *   `client_socket.close()`

*   **Servidor:**
    1.  Encerramento da thread que lidava com o cliente.
    2.  O servidor continua rodando, aguardando novas conexões.

**Observações:**

*   **Tratamento de Erros:** Em cada etapa, o código inclui tratamento de erros para lidar com possíveis problemas (conexão, criptografia, leitura de dados, etc.).
*   **Threads:** O uso de threads é crucial para que o servidor possa lidar com múltiplos clientes de forma concorrente.
*   **Segurança:** A criptografia garante a confidencialidade dos dados durante a transmissão.
*   **Classes e Módulos:** A organização do código em classes e módulos facilita a manutenção e a reutilização.
