from tkinter import *
import socket
import pyaudio
from threading import Thread
from connexion import ClientTel
from telephone import appel1
import select


def appel(ip):
    global CHUNK
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    ip = ip.split()
    ip = ip[0]
    print(ip)

    global s
    print(ip)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,6000))

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

if __name__ == "__main__":
    appel("127.0.0.1")