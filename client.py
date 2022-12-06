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
        self.__socket_echange = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def connexion(self) -> None:
        try:
            self.__socket_echange.connect((self.__ip_serveur, self.__port_serveur))
            print("Connecté au serveur")
        except Exception as err:
            print("erreur : " + str(err))
    
    def envoyer(self, b:list[bytes], address = ("127.0.0.1", 5001))-> None:
        for byte in b:
            self.__socket_echange.sendto(byte, address)

    
    def enregistrement(self):
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print ("Enregistrement en cours...")

        frames : list = []
        
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            print (data)

            frames.append(data)
        print ("Fin d'enregistrement")

        for octet in frames :
            frames = data.extend(bytearray(frames))

        return frames

if __name__ == "__main__":

    ip = "127.0.0.1"
    port = 5001

    client : Client = None

    client = Client(ip,port)
    client.connexion()
    frames = client.enregistrement()
    client.envoyer(frames)

   