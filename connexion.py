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

