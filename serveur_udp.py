import socket
import select

class ChatServeur:
    def __init__(self):
        self.__socket_echange: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket_echange.bind(("127.0.0.1", 50000))
        self.__addr_client = "127.0.0.1"

        self.CONNECTION_LIST = []

        print("Serveur Vocal Initialisé")

    def recevoir_client(self):
        tab_bytes, self.__addr_client = self.__socket_echange.recvfrom(1024)
        print(self.__addr_client)
        print(f"adresse machine distante : {self.__addr_client}")


    def broadcast(self, sock, data):
        for current_socket in self.CONNECTION_LIST:
            if current_socket != self.__socket_echange and current_socket != sock:
                try:
                    current_socket.send(data)
                except:
                    pass

    def run(self):
        while True:
            try:
                data = self.__socket_echange.recv(1024)
                print(data.decode())
                self.broadcast(self.__socket_echange, data)
            except socket.error:
                print("left the server")
                self.__socket_echange.close()
                self.CONNECTION_LIST.remove(self.__socket_echange)

if __name__ == "__main__":
    serveur_udp = ChatServeur()
    serveur_udp.recevoir_client()
    serveur_udp.run()
