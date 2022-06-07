from listener import Listener
from sender import Sender

def main():
    endereco_peer = input("Endereço do peer: ")
    Listener().start()
    Sender(endereco_peer).start()

if __name__ == "__main__":
    main()
