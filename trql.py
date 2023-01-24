import socket
import pyaudio

def test():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


        print("Je envoie")
        fermeture_port = False
        global apparaitre
        apparaitre = False
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)
        server_socket.bind(("",6000))
        print(p.get_default_input_device_info())

        envoie = None 

        while True:
                msg,client_addr = server_socket.recvfrom(1024)
                print('GOT connection from ',client_addr)
                
                while True:
                        envoie = stream.read(1024)
                        server_socket.sendto(envoie,client_addr)
                        client_addr = server_socket.recvfrom(1024)
                        stream.write()

                
test()