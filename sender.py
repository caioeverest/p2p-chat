import select
import sys
import socket
import threading
import config
from _thread import start_new_thread

class Sender(threading.Thread):
    def __init__(self, endereco = '127.0.0.1', porta = config.SERVER_PORT):
        threading.Thread.__init__(self)
        endereco = '127.0.0.1' if endereco == '' else endereco
        print(f"Se conectando ao endereço {endereco} na porta {porta}")
        self.endereco = endereco
        self.porta = porta
        self.endereco_local = None if endereco == '' or endereco == '127.0.0.1' else '127.0.0.1'

    def handle_p2p_message(self, servidor, endereco):
        if not self.endereco_local: return
        servidor_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_local.connect((self.endereco_local, self.porta))
        while True:
            sockets_list = [sys.stdin, servidor_local]
            read_sockets, _, _= select.select(sockets_list,[],[])
            for socks in read_sockets:
                if socks == servidor_local:
                    msg = socks.recv(config.BUFFER_SIZE)
                    if endereco in msg.decode(): continue
                    servidor.send(msg)
                    sys.stdout.flush()

    def run(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.connect((self.endereco, self.porta))
        start_new_thread(self.handle_p2p_message, (servidor, self.endereco))
        while True:
            sockets_list = [sys.stdin, servidor]
            read_sockets, _, _= select.select(sockets_list,[],[])

            for socks in read_sockets:
                if socks == servidor:
                    msg = socks.recv(config.BUFFER_SIZE)
                    print (msg.decode())
                else:
                    msg = sys.stdin.readline()
                    servidor.send(bytes(msg,"ascii"))
                    sys.stdout.write("<Eu> ")
                    sys.stdout.write(msg)
                    sys.stdout.flush()
                    if msg.lower() == config.PALAVRA_CHAVE_SAIDA: return

