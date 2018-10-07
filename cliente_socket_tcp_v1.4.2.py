import socket, time, pickle, os

GBYTES = (1024 * 1024 * 1024)

# Mostra a informações da CPU:
def mostraUsoCpu(list):

    dic = {}
    for j in list[1]:
        # print(str(j))
        brand = list[1]['brand']
        arch = list[1]['arch']
        bits = list[1]['bits']
        freq = list[1]['hz_actual']
        count = list[1]['count']
        dic['Nome'] = brand
        dic['Arquitetura'] = arch
        dic['Palavra'] = bits
        dic['Frequencia'] = freq
        dic['Nucleos'] = count
    print()
    print('ARQUITETURA DA CPU:''\n')
    print('Nome:', dic['Nome'], '\n''Arquitetura:', dic['Arquitetura'],
          '\n''Palavra (bits):', dic['Palavra'], '\n''Frequência: ', dic['Frequencia'],
          '\n''Nucleos: ', dic['Nucleos'], '(' + str(list[2]) + ')')
    print()

    print('PERCENTUAL DE USO DA CPU POR NÚCLEO:''\n')
    for i, elem in enumerate(list[0]):
        # print(str(i))
        if len(list[0]) == 1:
            print('Core:'+ str(i))
            load("|", "|", 35, elem)
        else:
            print('Core:' + str(i))
            load("|", "|", 35, elem)
    print()

# Mostra a capacidade de MP em uso e total:
def mostraUsoMemoria(list):
    for mem in list:
        # print(i)
        total = round(mem.total/GBYTES, 2)
        totalEmUso = round(mem.used/GBYTES, 2)
        totalLivre = round(mem.free/GBYTES, 2)
        memPercent = round(mem.percent, 2)
        print('INFORMAÇÕES MEMÓRIA PRINCIPAL:''\n')
        print('Capacidade total: ' + str(total) + ' GB \n')
        print('Capacidade em uso: ' + str(totalEmUso) + ' GB')
        load("|", "|", 35, memPercent)
        print('\n''Capacidade livre: ' + str(totalLivre) + ' GB''\n')

# Mostra a capacidade do disco rígido em uso e total:
def mostraUsoDisco(list):
    for disco in list:
        #print(disco)
        total = round(disco.total/GBYTES, 2)
        discoUso = round(disco.used/GBYTES, 2)
        discoLivre = round(disco.free/GBYTES, 2)
        discoPercent = round(disco.percent, 2)
        print('INFORMAÇÕES DISCO RÍGIDO:''\n')
        print('Capacidade total: ' + str(total) + ' GB \n')
        print('Capacidade em uso: ' + str(discoUso) + ' GB')
        load("|", "|", 35, discoPercent)
        print('\n''Capacidade disponível: ' + str(discoLivre) + ' GB\n')

# Mostra informações de diretórios, arquivos e sistema de arquivos
def mostraInfoDir(list):

    print('ARQUIVOS E DIRETÓRIOS:\n')
    list_partition = []
    for i in list[0]:
        list_partition.append(i)
    # print(list_partition)
    if list_partition:
        titulo_partition = '{:^15}'.format("DEVICE")
        titulo_partition = titulo_partition + '{:^20}'.format("POINT MOUNT")
        titulo_partition = titulo_partition + '{:^35}'.format("FILE SYSTEM")
        print(titulo_partition)

        for j in list_partition:
            # print(j)
            device = j[0]
            mount = j[1]
            sys_file = j[2]
            print("\t" + '{:<15}'.format(device) + '{:<28}'.format(mount)
                  + '{:<10}'.format(sys_file))
    print()

    if list[1]:
        titulo = '{:^13}'.format('TAMANHO')
        titulo = titulo + '{:^25}'.format('DATA DE CRIAÇÃO')
        titulo = titulo + '{:^33}'.format('DATA DE MODIFICAÇÃO')
        titulo = titulo + '{:^27}'.format('NOME')
        print(titulo)

    for key in list[1]:
        #print(list[1][key])
        file_name = '{:<30}'.format(key)
        for i in list[1][key]:
            kb = list[1][key][0]/1024
            tam = '{:>10}'.format(str('{:.2f}'.format(kb) + ' KB'))
            c_time = '{:^32}'.format(time.ctime((list[1][key][1])))
            m_time = '{:<30}'.format(time.ctime((list[1][key][2])))
        print(str(tam + c_time + m_time + file_name))
    print()

# Mostra informações de processos em execução
def print_info_process(list):

    print('PROCESSOS:\n')
    percentual = 2
    if list:
        titulo = '\t''{:<6}'.format("PID")
        titulo = titulo + '{:^20}'.format("Name")
        titulo = titulo + '{:^6}'.format("%CPU")
    print(titulo)

    lista_ordenada = sorted(list, key=func_comparation, reverse=True)
    for i in lista_ordenada:
        if i['cpu_percent'] >= (percentual):
            texto = '\t''{:<6}'.format(i['pid'])
            texto = texto + '{:^20}'.format(i['name'])
            texto = texto + '{:>6}'.format(i['cpu_percent'])
            print(texto)
            #time.sleep(0.2)
    print()

# Mostra informações de rede
def print_info_net(list, list_st):
    #print(list)
    print('INTERFACES DE REDE:\n')
    nomes = []
    # Obtém os nomes das interfaces
    for key in list[0]:
        nomes.append(str(key))

    if nomes:
        titulo = '{:13}'.format("INTERFACES")
        titulo = titulo + '{:>13}'.format("FAMILY")
        titulo = titulo + '{:>20}'.format("ADDRESS")
        titulo = titulo + '{:>20}'.format("NETMASK")
        titulo = titulo + '{:>20}'.format("BROADCAST")
        print(titulo)

    for i in nomes:
        print(i + ':')
        values_tuple = []
        for a, b, c, d, _, in list[0][i]:
            #print(a)
            values_tuple.append(a)
            values_tuple.append(b)
            values_tuple.append(c)
            values_tuple.append(d)
            #print(list_fam)
        for j in values_tuple:
            family = str(values_tuple[0])
            address = str(values_tuple[1])
            netmask = str(values_tuple[2])
            broadcast = str(values_tuple[3])
        print('\t' + '{:^29}'.format(family) + '{:<20}'.format(address)
              + '{:<17}'.format(netmask) + '{:<20}'.format(broadcast))
    print()
    input('Pressione qualquer tecla para continuar...')
    print()

    print('STATUS:\n')
    nameStatus = []
    # Obtém os nomes das interfaces
    for k in list_st[0]:
        nameStatus.append(str(k))

    if nameStatus:
        titulo = '{:>18}'.format("ISUP")
        titulo = titulo + '{:>20}'.format("DUPLEX")
        titulo = titulo + '{:>20}'.format("SPEED")
        titulo = titulo + '{:>8}'.format("MTU")
        print(titulo)

    for l in nameStatus:
        print(l + ':')
        isup = str(list_st[0][l][0])
        duplex = str(list_st[0][l][1])
        speed = str(list_st[0][l][2])
        mtu = str(list_st[0][l][3])
        print("\t" + '{:^14}'.format(isup) + '{:<33}'.format(duplex)
              + '{:<7}'.format(speed) + '{:<8}'.format(mtu))
    print()
    input('Pressione qualquer tecla para continuar...')
    print()

    print('ENTRADA E SAIDA DE DADOS:\n')
    names_Io_status = []
    for m in list_st[1]:
        names_Io_status.append(str(m))

    if names_Io_status:
        titulo = '{:>20}'.format("BYTES_SENT")
        titulo = titulo + '{:>14}'.format("BYTES_RECV")
        titulo = titulo + '{:>15}'.format("PACKETS_SENT")
        titulo = titulo + '{:>15}'.format("PACKETS_RECV")
        print(titulo)

    for n in names_Io_status:
        print(n + ':')
        bytes_sent = str(list_st[1][n][0])
        bytes_recv = str(list_st[1][n][1])
        packets_sent = str(list_st[1][n][2])
        packets_recv = str(list_st[1][n][3])
        print("\t" + '{:^4}'.format(' ') + '{:<12}'.format(bytes_sent) + '{:<15}'.format(bytes_recv)
              + '{:<15}'.format(packets_sent) + '{:<10}'.format(packets_recv))
    print()
    input('Pressione qualquer tecla para continuar...')
    print()

    print('CONEXÕES:\n')
    list_con = []
    for i in list_st[2]:
        list_con.append(i)
        # print(list_con)

    if list_con:
        titulo = '{:>4}'.format("FD")
        titulo = titulo + '{:>16}'.format("FAMILY")
        titulo = titulo + '{:>24}'.format("TYPE")
        # titulo = titulo + '{:>20}'.format("LADDR")
        # titulo = titulo + '{:>15}'.format("RADDR")
        titulo = titulo + '{:>20}'.format("STATUS")
        titulo = titulo + '{:>11}'.format("PID")
        print(titulo)

    for j in list_con:
        fd = str(j[0])
        family = str(j[1])
        type = str(j[2])
        status = str(j[5])
        pid = str(j[6])
        print('{:^7}'.format(fd) + '{:<25}'.format(family) + '{:<25}'.format(type)
              + '{:<15}'.format(status) + '{:<10}'.format(pid))
    print()

# Imprime o status de download
def print_status_down(bytes, tam):
    kbytes = bytes/1024
    tam_bytes = tam/1024
    texto = 'Baixando... '
    texto = texto + '{:<.2f}'.format(kbytes) + ' KB '
    texto = texto + 'de ' + '{:<.2f}'.format(tam_bytes) + ' KB'
    print(texto)

def load(left_side, right_side, length, percent):
    x = 0
    y = ""
    p = length*percent/100
    #print("\r")
    while x <= p:
        space = length - len(y)
        space = " " * space
        z = left_side + y + space + right_side
        y += "█"
        time.sleep(0.1)
        x += 1
    print("\r", 'Percentual:', str(percent) + '%', z)

def clear():
   os.system("cls" if os.name == "nt" else "clear")

def func_comparation(l):
    return(l['cpu_percent'])

def print_menu():  # Função que exibe menu de exibição

    print(80 * '*')
    print('*', '{:^76}'.format(' '), '*''\n''*', '{:^76}'.format('MONITOR DO SISTEMA'),
          '*''\n''*', '{:^76}'.format(' '), '*')
    print(80 * '*')

    print(37 * "*", "MENU", 37 * "*")
    print("1. CPU")
    print("2. MEMÓRIA")
    print("3. DISCO")
    print("4. DIRETÓRIOS")
    print("5. PROCESSOS")
    print("6. REDES")
    print("7. DOWNLOADS")
    print("8. SAIR")
    print(80 * "*")

serverHost = socket.gethostname()
serverPort = 30000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conecta-se ao servidor
    client.connect((serverHost, serverPort))
    data = ' '
    loop = True
    while loop:  # Enquanto loop = True continuará até loop = False

        print_menu()  # Menu de exibição
        choice = int(input("Digite uma opção [1-8]: "))
        print()

        if choice == 1:
            clear()
            sair = True
            while sair:
                data = '1'
                # Envia mensagem vazia apenas para indicar a requisição
                client.send(data.encode('utf-8'))
                # Recebe reposta da requisição
                bytes = client.recv(2048)
                # Converte os bytes para lista
                list = pickle.loads(bytes)
                mostraUsoCpu(list)
                #time.sleep(1)
                voltaMenu = int(input('Digite zero[0] para voltar ao Menu: '))
                if voltaMenu == 0:
                    sair = False

        if choice == 2:
            clear()
            sair = True
            while sair:
                data = '2'
                # Envia mensagem vazia apenas para indicar a requisição
                client.send(data.encode('utf-8'))
                # Recebe reposta da requisição
                bytes = client.recv(1024)
                # Converte os bytes para lista
                list = pickle.loads(bytes)
                mostraUsoMemoria(list)
                # time.sleep(1)
                voltaMenu = int(input('Digite zero[0] para voltar ao Menu: '))
                if voltaMenu == 0:
                    sair = False

        if choice == 3:
            clear()
            sair = True
            while sair:
                data = '3'
                # Envia mensagem vazia apenas para indicar a requisição
                client.send(data.encode('utf-8'))
                # Recebe reposta da requisição
                bytes = client.recv(1024)
                # Converte os bytes para lista
                list = pickle.loads(bytes)
                mostraUsoDisco(list)
                # time.sleep(1)
                voltaMenu = int(input('Digite zero[0] para voltar ao Menu: '))
                if voltaMenu == 0:
                    sair = False

        if choice == 4:
            clear()
            sair = True
            while sair:
                data = '4'
                # Envia mensagem vazia apenas para indicar a requisição
                client.send(data.encode('utf-8'))
                msg = client.recv(1024)
                mensagem = ''
                mensagem += msg.decode()
                print(mensagem)
                dir = input('Entre com o nome do diretório: ')
                client.send(dir.encode('utf-8'))
                # Recebe reposta da requisição
                bytes = client.recv(2048)
                # Converte os bytes para listamostraInfoDir(list)
                list = pickle.loads(bytes)
                mostraInfoDir(list)
                # time.sleep(1)
                voltaMenu = int(input('Digite zero[0] para voltar ao Menu: '))
                if voltaMenu == 0:
                    sair = False

        if choice == 5:
            clear()
            sair = True
            while sair:
                data = '5'
                # Envia mensagem vazia apenas para indicar a requisição
                client.send(data.encode('utf-8'))
                # Recebe reposta da requisição
                bytes = client.recv(50000)
                # Converte os bytes para lista
                list = pickle.loads(bytes)
                print_info_process(list)
                # time.sleep(1)
                voltaMenu = int(input('Digite zero[0] para voltar ao Menu: '))
                if voltaMenu == 0:
                    sair = False

        if choice == 6:
            clear()
            sair = True
            while sair:
                data = '6'
                # Envia mensagem vazia apenas para indicar a requisição
                client.send(data.encode('utf-8'))
                # Recebe reposta da requisição
                bytes1 = client.recv(50000)
                # Converte os bytes para lista
                list1 = pickle.loads(bytes1)

                # Recebe reposta da requisição
                bytes2 = client.recv(50000)
                # Converte os bytes para lista
                list2 = pickle.loads(bytes2)

                print_info_net(list1, list2)

                voltaMenu = int(input('Digite zero[0] para voltar ao Menu: '))
                if voltaMenu == 0:
                    sair = False

        if choice == 7:
            clear()
            sair = True
            while sair:
                data = '7'
                client.send(data.encode('utf-8'))
                data = client.recv(1024)
                #print(data)
                data = input('Entre com o nome do arquivo: ')
                client.send(data.encode('utf-8'))
                # Recebe o tamanho do arquivo:
                data = client.recv(12)
                tamanho = int(data.decode('utf-8'))
                # Checa se o arquivo existe no servidor:
                if tamanho >= 0:
                    # Gera o arquivo local
                    novo_nome = input('Defina um novo nome: ')
                    arq = open(novo_nome, "wb")
                    soma = 0
                    bytes = client.recv(4096)
                    # Escreve o arquivo
                    while bytes:
                        arq.write(bytes)
                        soma = soma + len(bytes)
                        print_status_down(soma, tamanho)
                        bytes = client.recv(4096)
                    #Fecha o arquivo
                    arq.close()
                else:
                    print('Arquivo não encontrado no servidor!\n' + 'Código de erro: ' + str(tamanho))

                voltaMenu = int(input('Digite zero[0] para voltar ao Menu: '))
                if voltaMenu == 0:
                    sair = False
            
        if choice == 8:
            data = '8'
            client.send(data.encode('utf-8'))
            print("Saindo do programa...")
            loop = False  # Isso fará com que o loop do while termine

        else:
            # Qualquer entrada inteira diferente dos valores 1-8, imprimirá uma mensagem de erro
            print("Seleção de opções erradas. Insira qualquer tecla para tentar novamente ..")

    
except Exception as error:
    print(str(error))

# Fecha o socket
client.close()
input('Pressione qualquer tecla para sair...')