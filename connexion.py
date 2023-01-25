# ---------------------------------------
# Projet : Téléphonie en Python
# Auteurs : Eliot GUESDON, Mattéo ROBIN, Loic HARRANG
# Fichier : connexion.py
# Objectif : Fichier de vérification des numéro (bon format) + envoie au serveur central du numéro vérifié et de sont mot clé (instruction) correspondant
# ---------------------------------------

import socket

class ClientTel:
    def __init__(self, ipserveur: str, portserveur: int):
        ipserveur = ipserveur.rstrip()
        self.__ipserveur = ipserveur
        self.__portserveur = portserveur
        self.__socket: socket = None
        self.__connexion_ok: bool = True

        try:
            # Initialisation du modèle TCP
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connexion au serveur central
            self.__socket.connect((self.__ipserveur, self.__portserveur))
            print("Connecté au serveur")
            self.__connexion_ok = True

        except socket.error as serr:
            # Si erreur lors de la connexion, affichage de l'erreur
            print("erreur de connexion au serveur :", serr)
            self.__connexion_ok = False

    def get_connexion(self) -> bool: # Fonction qui retourne l'etat de connexion au serveur central (True ou False)
        return self.__connexion_ok

    def enregistrement(self, num: int): # Fonction qui test le numéro passé en paramètre et si ok, envoie le numéro au serveur central
        res: str = ""
        test: bool = False
        print(num)
        cherch = "CHERCHER:"
        # Test du format du numéro de téléphone (RAPPEL : 3 chiffres)
        try:
            if num != '':
                num = str(num)
                num = cherch + num # Concaténation du mot-clé CHERCHER: + le numéro
                print(num)
                test = True
            else:
                pass

        except:
            test = False

        print(type(num))
        if test == True:
            self.envoyer(num) # Appel de la fonction envoyer (avec le numéro destinataire)
            res = self.recevoir() # Appel de la fonction recevoir
        else:
            res = "Format Incorrect"
        return res

    def destinataire(self, num_appeler): # Fonction qui test le numéro passé en paramètre et si ok, envoie une confirmation au serveur central
        res: str = ""
        test: bool = False
        print(num_appeler)
        # Test du format du numéro de téléphone (RAPPEL : 3 chiffres)
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
            self.envoyer(f"APL:{num_appeler}") # Envoie du mot clé APL: + numéro à appeler
            res = self.recevoir() # Appel de la fonction recevoir
        else:
            res = "non existant"
        print(res)
        return res

    def envoyer(self, msg: str) -> None: # Fonction d'envoie d'un numéro au serveur central
        tab_byte = msg.encode("utf-8") # Encodage du message en UTF-8
        self.__socket.send(tab_byte) # Envoie des donnée encodées

    def recevoir(self) -> str: # Fonction qui permet de recevoir une confirmation de la part du serveur
        tab_bytes: bytes = self.__socket.recv(255)
        msg: str = tab_bytes.decode("utf-8") # Décodage du message reçu
        return msg
