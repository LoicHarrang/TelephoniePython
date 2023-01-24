import socket
from threading import Thread
import pyaudio


def test(ip):
        chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        print("ecoute commence")
        fermeture_port = False
        global apparaitre
        apparaitre = False
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

        print(p.get_default_input_device_info())
        clientsocket : socket = (ip,6000)

        while True:
                envoie = stream.read(10)
                chat_server_socket.sendto(envoie,(clientsocket))
                
                
                while True:
                        msg,client_addr = chat_server_socket.recvfrom(1024)
                        print('GOT connection from ',client_addr,msg)
                        stream.write(msg)
                        
                

test("127.0.0.1")