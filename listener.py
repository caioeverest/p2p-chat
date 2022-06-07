import socket
import threading
from _thread import start_new_thread
import config

class Listener(threading.Thread):
    def __init__(self, endereco = '0.0.0.0', porta = config.SERVER_PORT):
        threading.Thread.__init__(self)
        print(f"Iniciando o servidor no endereço {endereco} e na porta {porta}")
        self.endereco = endereco
        self.port = porta
        self.lista_clientes = []

    def thread_worker(self, conn, endereco):
        conn.send(bytes("Bem vindo ao chat de Redes I!", "ascii"))
        while True:
            try:
                msg = conn.recv(config.BUFFER_SIZE).decode()
                if msg:
                    if msg.lower() == f"<{endereco[0]}> {config.PALAVRA_CHAVE_SAIDA}":
                        message_to_send = f"Conexão {endereco[0]} saiu do chat"
                        self.broadcast(message_to_send, conn ,endereco[0])
                        self.lista_clientes.remove(conn)
                    elif endereco[0] in msg:
                        self.broadcast(msg, conn ,endereco[0])
                    else:
                        message_to_send = f"<{endereco[0]}> {msg}"
                        self.broadcast(message_to_send, conn, endereco[0])
                else:
                    self.lista_clientes.remove(conn)
            except:
                continue

    def broadcast(self, msg, connection, endereco):
        for conn in self.lista_clientes:
            if conn != connection and endereco in msg:
                try:
                    conn.send(bytes(msg, 'ascii'))
                except Exception as error:
                    print(f"Erro no broadcast - {error}")
                    conn.close()
                    self.lista_clientes.remove(conn)

    def run(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((self.endereco, self.port))
        servidor.listen(100)
        while True:
            conn, endereco = servidor.accept()
            self.lista_clientes.append(conn)
            start_new_thread(self.thread_worker, (conn,endereco))
