import socket
import sys
import os
import pyaudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
  
audio = pyaudio.PyAudio()

class ServiceEcoute:

    def __init__(self, port_serveur: int)-> None:
        self.__port_serveur = port_serveur
        self.socket_ecoute: socket

    def attente(self)-> socket:
        self.socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_ecoute.bind(("", self.__port_serveur))
        self.socket_ecoute.listen(1)
        print(f"serveur en ecoute sur le port {self.__port_serveur} ...")

        socket_echange, ADDR = self.socket_ecoute.accept()
        print("une nouvelle demande de connexion")
        print(f"sochet echange : {socket_echange}")
        #print(f"adr : {ADDR}")
        return socket_echange


class ServiceEchange:
    def __init__(self, socket_echange: socket)-> None:
        self.__socket_echange = socket_echange

    def envoyer(self, msg: str)-> None:
        tab_bytes = msg.encode("utf-8")
        self.__socket_echange.send(tab_bytes)

    def recevoir(self)-> str:
        frames = self.__socket_echange.recv(1024)
        return frames


    def echange(self)->None:
        fin: bool = False
        while(not fin):
            recu = self.recevoir()
            if recu == "fin":
                fin = True
            print(f"C => S : {recu}")

            # preparation de la réponse
            msg_serveur = f"[{recu}]"
            self.envoyer(msg_serveur)

if __name__ == "__main__":
    # declaration des variables
    port_ecoute: int = None
    service_ecoute: ServiceEcoute = None
    socket_client: socket = None
    service_echange: ServiceEchange = None
    # lecture des parametres (le numero de port)
    if len(sys.argv) >= 2:
        port_ecoute = int(sys.argv[1])
    else:
        port_ecoute = 5001
    #try:
    service_ecoute = ServiceEcoute(port_ecoute)
    socket_client = service_ecoute.attente()
    service_echange = ServiceEchange(socket_client)
    frames = service_echange.recevoir()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    for data in frames:
        stream.write(data)
    #except Exception as err:
        #print("erreur : " + str(err))