import socket
import threading

SERVER = 'localhost'
PORT = 5002
ADDR = (SERVER, PORT)
PORT_ADDRS = [5003, 5001]
FORMATO = 'UTF-8'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
ultima_mensagem = [1]


def recebimento_Server(conn, addr, PORT_ADDRS):
    while True:
        msg = conn.recv(1024).decode(FORMATO)
        if not msg:
            break
        print(f"O Usuário: {addr} Mandou Mensagem!")
        print(f"Ele Mandou: [{msg.split('+')[-1]}] que Veio Pela Porta [{msg.split('+')[-2]}]")
        try:
            if ultima_mensagem[-1] == msg:
                response = f'Essa Dai eu Já Ouvi!!\n'
                print(f'EU: {response}')
                conn.send(response.encode(FORMATO))
            else:
                response = f'ME CONTE MAIS!\n'
                ultima_mensagem.append(msg)
                print(f'EU: {response}\n')
                conn.send(response.encode(FORMATO))
                replicate_thread = threading.Thread(target=repasse_Cliente, args=[PORT_ADDRS, msg])
                replicate_thread.start()
        except:
            print('Erro ao responder.')


def server(server_socket, PORT_ADDRS):
    while True:
        server_socket.listen()
        conn, addr = server_socket.accept()

        tw = threading.Thread(target=recebimento_Server, args=[conn, addr, PORT_ADDRS])
        tw.start()


def repasse_Cliente(PORT_ADDRS, msg):
    print('\n\t\tVou Repassar a Fofoca!\n')
    rc = True
    while rc:
        for port in PORT_ADDRS:
            port_vizinho = ('localhost', int(port))
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            try:
                client_socket.connect(port_vizinho)
                client_socket.send(msg.encode(FORMATO))

                response, server = client_socket.recvfrom(1024)
                print(f'O Vizinho Respondeu: {response.decode(FORMATO)}\n')
                client_socket.shutdown(socket.SHUT_RDWR)
            except:
                print('\n\t\t[Erro ao Repassar a Mensagem!]\n')
            if PORT_ADDRS[-1] == port:
                rc = False


def mensagem_Cliente(PORT_ADDRS):
    while True:
        msg = input('Mande Uma Mensagem!\n')
        msg = f'{PORT}+{msg}'
        ultima_mensagem.append(msg)
        for port in PORT_ADDRS:
            port_vizinho = ('localhost', int(port))
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            try:
                client_socket.connect(port_vizinho)
                client_socket.send(msg.encode(FORMATO))
            except:
                print('\n\t\t[Cliente NÃO Conectado ou Ocorreu um Erro]\n')


client_thread = threading.Thread(target=mensagem_Cliente, args=[PORT_ADDRS])
receiver_thread = threading.Thread(target=server, args=[server_socket, PORT_ADDRS])
receiver_thread.start()
client_thread.start()
