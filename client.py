import pyaudio
import socket
import sys

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
  
audio = pyaudio.PyAudio()

class Client:
    def __init__(self, ip_serveur: str, port_serveur: int) -> None:
        self.__ip_serveur = ip_serveur
        self.__port_serveur = port_serveur
        self.__socket_echange = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connexion(self) -> None:
        try:
            self.__socket_echange.connect((self.__ip_serveur, self.__port_serveur))
            print("Connecté au serveur")
        except Exception as err:
            print("erreur : " + str(err))
    
    def envoyer(self, msg: str)-> None:
        tab_bytes = msg.encode("utf-8")
        self.__socket_echange.send(tab_bytes)
    
    def recevoir(self)-> str:
        tab_bytes = self.__socket_echange.recv(255)
        msg = tab_bytes.decode("utf-8")
        return msg
    
    def echange(self)->None:
        fin = False
        while(not fin):
            msg = input("votre message : ")
            self.envoyer(msg)
            recu = self.recevoir()
            print(f"S=>C : {recu}")
            if recu == "[fin]":
                fin = True
        
        print("Connexion fermée")
        self.__socket_echange.close()


if __name__ == "__main__":
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print ("Enregistrement en cours...")

    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print ("Fin d'enregistrement")

    ip = "127.0.0.1"
    port = 5000

    client : Client = None

    client = Client(ip,port)
    client.connexion()
    client.envoyer(frames)