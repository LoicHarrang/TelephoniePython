import sys
import socket
from typing import List
import select

class ClientTel:
    def __init__(self,ipserveur: str ,portserveur: int ):
        ipserveur = ipserveur.rstrip()
        self.__ipserveur = ipserveur
        self.__portserveur = portserveur
        self.__socket: socket = None
        self.__connexion_ok: bool = True

        try:
            # connexion
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the server
            self.__socket.connect((self.__ipserveur,self.__portserveur))
            print("Connecté au serveur")
            self.__connexion_ok = True

        except socket.error as serr:
            print("erreur de connexion au serveur :",serr)
            self.__connexion_ok = False

    def get_connexion(self)->bool:
        return self.__connexion_ok


    def enregistrement(self,num : int):
        res : str = ""
        #Test si c'est le bon format
        test : bool = False
        print(num)
        cherch = "CHERCHER:"

        try:
            if num != '':
                num = str(num)
                num = cherch + num
                print(num)
                test = True
            else:
                pass

        except:
            test = False

        print(type(num))
        if test == True:
            self.envoyer(num)
            res = self.recevoir()
        else:
            res = "Pas bon format"
        return res

    def destinataire(self,num_appeler):
        res : str = ""
        #Test si c'est le bon format
        test : bool = False
        print(num_appeler)

        try:
            if num_appeler != '':
                num_appeler = str(num_appeler)
                test = True
            else:
                pass

        except:
            test = False

        print(type(num_appeler))
        print(num_appeler)

        if test == True:
            self.envoyer(f"APL:{num_appeler}")
            res = self.recevoir()
        else:
            res = "non existant"
        print(res)
        return res


    def envoyer(self, msg: str)-> None:
        tab_byte: tab_byte = msg.encode("utf-8")
        self.__socket.send(tab_byte)

    # la methode recevoir() est donnee
    def recevoir(self)-> str:
        tab_bytes: bytes = self.__socket.recv(255)
        msg: str = tab_bytes.decode("utf-8")
        return msg



class ChatServer:
    def __init__(self):

        self.CONNECTION_LIST = []
        self.chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_server_socket.bind(("127.0.0.1", 60000))
        self.chat_server_socket.listen(5)

        self.CONNECTION_LIST.append(self.chat_server_socket)

        print ("Server Started!")

    def broadcast(self, sock, data):
        for current_socket in self.CONNECTION_LIST:
            if current_socket != self.chat_server_socket and current_socket != sock:
                try:
                    current_socket.send(data)
                except:
                    pass

    def run(self):
        while True:
            rlist, wlist, xlist = select.select(self.CONNECTION_LIST, [], [])

            for current_socket in rlist:
                if current_socket is self.chat_server_socket:
                    (new_socket, address) = self.chat_server_socket.accept()
                    self.CONNECTION_LIST.append(new_socket)
                    print("connected to the server")
                else:
                    try:
                        data = current_socket.recv(1024)
                        self.broadcast(current_socket, data)
                    except socket.error:
                        print("left the server")
                        current_socket.close()
                        self.CONNECTION_LIST.remove(current_socket)