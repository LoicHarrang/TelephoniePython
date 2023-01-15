import pyaudio
import socket
from threading import Thread

def appel1():
    global CHUNK
    CHUNK = 1024 
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1",6000))
    

    thread_ecoute = Thread(target=receive_data)
    thread_enregistrer = Thread(target=send_data)


    p = pyaudio.PyAudio()
    connexion = True
    print("Le chat vocal va commencer")

    global receive_stream
    global send_stream
    receive_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    send_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)



    if connexion == True:
        thread_ecoute.start()
        thread_enregistrer.start()
        thread_ecoute.join()
        thread_enregistrer.join()

    

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
