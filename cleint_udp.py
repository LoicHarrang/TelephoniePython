import socket
from threading import Thread
import pyaudio

# record
CHUNK = 1024 # 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000

p = pyaudio.PyAudio()

receive_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
send_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
class Client_UDP(Thread):
    def __init__(self, ip_serveur: str, port_serveur: int) -> None:
        self.__ip_serveur: str = ip_serveur
        self.__port_serveur = port_serveur
        self.__socket_echange: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__fin: bool = False
        self.__thread_envoyer: Thread = Thread(target=self.envoyer, args=())

    def envoyer(self) -> None:
        while not self.__fin:
            msg = input('Votre message:')
            tab_bytes = msg.encode("utf-8")
            self.__socket_echange.sendto(tab_bytes, (ip_serveur, self.__port_serveur))

    def receive_data(self):
        while True:
            try:
                data = self.__socket_echange.recv(1024)
                receive_stream.write(data)
            except:
                pass

    def send_data(self):
        while True:
            try:
                data = send_stream.read(CHUNK)
                self.__socket_echange.sendall(data)
            except:
                pass

if __name__ == "__main__":
    # declaration des variables
    ip_serveur: str = None
    port_serveur: int = None
    client_udp: Client_UDP
    connexion = True

    # initialisation
    ip_serveur = "127.0.0.1"
    port_serveur = 50000

    # instanciation:
    client_udp = Client_UDP(ip_serveur=ip_serveur, port_serveur=port_serveur)
    thread_ecoute = Thread(target=client_udp.receive_data)
    thread_enregistrer = Thread(target=client_udp.send_data)

    if connexion == True:
        thread_ecoute.start()
        thread_enregistrer.start()
        thread_ecoute.join()
        thread_enregistrer.join()