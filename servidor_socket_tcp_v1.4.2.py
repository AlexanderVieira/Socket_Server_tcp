import socket, os, psutil, cpuinfo, pickle

# Obtem nome e porta da máquina
myHost = socket.gethostname()
myPort = 30000

# Cria o socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa ip e porta
server.bind((myHost, myPort))

# Servidor esperando por uma conexão
server.listen()
print('Servidor:', myHost, 'esperando conexão na porta:', myPort)

# Aceita alguma conexão
(conexao, address) = server.accept()
print('Conectado a:', str(address))

while True:
    # Recebe requisicão do cliente
    data = ''
    data = conexao.recv(2048)

    if data.decode('utf-8') == '1':
        request = data.decode('utf-8')
        print('Requisição da opção', request, 'recebida com sucesso!')
        print('Processando...')
        list_percent_cpu = psutil.cpu_percent(interval= 1, percpu= True)
        dict_info_cpu = cpuinfo.get_cpu_info()
        num_cores = psutil.cpu_count(logical=True)
        # Cria a lista de resposta
        response = []
        response.append(list_percent_cpu)
        response.append(dict_info_cpu)
        response.append(num_cores)
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(response)
        # Envia os dados
        conexao.send(bytes_resp)
        print('Resposta da opção', request, 'enviada com sucesso!\n')

    if data.decode('utf-8') == '2':
        request = data.decode('utf-8')
        print('Requisição da opção', request, 'recebida com sucesso!')
        print('Processando...')
        info_mem = psutil.virtual_memory()
        # Cria a lista de resposta
        response = []
        response.append(info_mem)
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(response)
        # Envia os dados
        conexao.send(bytes_resp)
        print('Resposta da opção', request, 'enviada com sucesso!\n')

    if data.decode('utf-8') == '3':
        request = data.decode('utf-8')
        print('Requisição da opção', request, 'recebida com sucesso!')
        print('Processando...')
        info_disco = psutil.disk_usage('.')
        # Cria a lista de resposta
        response = []
        response.append(info_disco)
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(response)
        # Envia os dados
        conexao.send(bytes_resp)
        print('Resposta da opção', request, 'enviada com sucesso!\n')

    if data.decode('utf-8') == '4':
        request = data.decode('utf-8')
        print('Requisição da opção', request, 'recebida com sucesso!')
        print('Processando...')
        msg = 'Diretório solicitado'
        conexao.send(msg.encode('utf-8'))
        nome_dir = conexao.recv(2048)
        dir = str(nome_dir.decode('utf-8'))
        list = os.listdir(dir)
        dict_file = {}
        for file in list:
            if os.path.isfile(file):
                dict_file[file] = []
                dict_file[file].append(os.stat(file).st_size)
                dict_file[file].append(os.stat(file).st_ctime)
                dict_file[file].append(os.stat(file).st_mtime)

        info_partitions = psutil.disk_partitions()
        # Cria a lista de resposta
        response = []
        response.append(info_partitions)
        response.append(dict_file)
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(response)
        # Envia os dados
        conexao.send(bytes_resp)
        print('Resposta da opção', request, 'enviada com sucesso!\n')


    if data.decode('utf-8') == '5':
        request = data.decode('utf-8')
        print('Requisição da opção', request, 'recebida com sucesso!')
        print('Processando...')
        for i in range(2):
            response = []
            list_proc = psutil.process_iter()
            for proc in list_proc:
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
                    response.append(pinfo)
                    # Prepara a lista para o envio

                except psutil.NoSuchProcess:
                    pass
        bytes_resp = pickle.dumps(response)
        # Envia os dados
        conexao.send(bytes_resp)
        print('Resposta da opção', request, 'enviada com sucesso!\n')

    if data.decode('utf-8') == '6':
        request = data.decode('utf-8')
        print('Requisição da opção', request, 'recebida com sucesso!')
        print('Processando...')
        dict_interface = psutil.net_if_addrs()
        # Cria a lista de resposta
        response = []
        response.append(dict_interface)
        # Prepara a lista para o envio
        bytes_resp1 = pickle.dumps(response)
        # Envia os dados
        conexao.send(bytes_resp1)

        status = psutil.net_if_stats()
        io_status = psutil.net_io_counters(pernic=True)
        conn = psutil.net_connections()
        # Cria a lista de resposta
        response_2 = []
        response_2.append(status)
        response_2.append(io_status)
        response_2.append(conn)
        # Prepara a lista para o envio
        bytes_resp2 = pickle.dumps(response_2)
        # Envia os dados
        conexao.send(bytes_resp2)
        print('Resposta da opção', request, 'enviada com sucesso!\n')

    if data.decode('utf-8') == '7':
        request = data.decode('utf-8')
        print('Requisição da opção', request, 'recebida com sucesso!')
        print('Processando...')
        data = 'Down'
        conexao.send(str(data).encode('utf-8'))
        data = conexao.recv(2048)
        nome_arq = str(data.decode('utf-8'))
        if os.path.isfile(nome_arq):
            # Envia primeiro o tamanho
            tamanho = os.stat(nome_arq).st_size
            conexao.send(str(tamanho).encode('utf-8'))
            # Abre o arquivo no modo leitura de bytes
            arq = open(nome_arq, 'rb')
            # Envia os dados
            bytes = arq.read(4096)
            while bytes:
                conexao.send(bytes)
                bytes = arq.read(4096)
            # Fecha o arquivo
            arq.close()
            print('Transferência concluída!')
        else:
            print("Não encontrou o arquivo")
            # tamanho é -1 para indicar que não achou arquivo
            conexao.send('-1'.encode('utf-8'))
        print('Resposta da opção', request, 'enviada com sucesso!\n')

    if data.decode('utf-8') == '8':
        print('Conexão encerrada.')
        break

# Fecha socket do servidor e cliente
conexao.close()
server.close()

