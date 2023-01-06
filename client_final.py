import socket
import pyaudio
import wave
from threading import Thread

# record
CHUNK = 1024 # 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 50000))

p = pyaudio.PyAudio()

receive_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
send_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)



def receive_data():
    while True:
        try:
            data = s.recv(1024)
            receive_stream.write(data)
        except:
            pass


def send_data():
    while True:
        try:
            data = send_stream.read(CHUNK)
            s.sendall(data)
        except:
            pass
        

if __name__ == "__main__":
    connexion = True
    print("Le chat vocal va commencer")
    thread_ecoute = Thread(target=receive_data)
    thread_enregistrer = Thread(target=send_data)
    if connexion == True:
        thread_ecoute.start()
        thread_enregistrer.start()
        thread_ecoute.join()
        thread_enregistrer.join()
