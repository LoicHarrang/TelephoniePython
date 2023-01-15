import socket
from threading import Thread
from socketserver import ThreadingMixIn
import sys
import sqlite3
import select

class ServeurTel:
    # constructeur
    def __init__(self, port: int):
        # attributs qui concerne le serveur
        self.__socket_serveur: socket
        self.__port: int = port
        # attributs qui concerne le client
        self.__socket_client: socket
        self.__service: ServiceEchange

        self.__socket_serveur = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_serveur.bind(("", self.__port))
        self.__socket_serveur.listen(1)

    def attenteClient(self) -> None:
        while (True):
            print(" ... attente client sur le port", self.__port, "...")
            self.__socket_client, addr = self.__socket_serveur.accept()
            print("Connexion avec : " + str(addr))
            self.__service = ServiceEchange(self.__socket_client)
            self.__service.echange()

    def arretServeur(self):
        if self.__socket_serveur != None:
            self.__socket_serveur.close()

    def arret_brutal_serveur(self):
        pass


class ServiceEchange:

    def __init__(self, socket_client) -> None:
        self.__socket_client: socket = socket_client


    def envoyer(self, msg: str) -> None:
        tab_byte: tab_byte = msg.encode("utf-8")
        self.__socket_client.send(tab_byte)

    def recevoir(self) -> str:
        tab_bytes: bytes = self.__socket_client.recv(255)
        msg: str = tab_bytes.decode("utf-8")
        return msg

    def echange(self) -> str:
        bonfrormat : bool = False
        fin_echange: bool = False
        longeur : int = 0
        while not fin_echange:
			# On lit la commande
            msg_client = self.recevoir()
            print(msg_client)

            try:
                variables = msg_client.split(":")
                mot_cle = variables[0]
                longeur = len(variables[1])
                msg_client = int(variables[1])
                bonfrormat = True               

            except:
                bonfrormat = False

            print(mot_cle)
            #Renvoie un message au client si pas bon
            if mot_cle == "CHERCHER":
                if bonfrormat == False or longeur != 3:
                    msg_serveur = "Pas bon format"
                    fin_echange = True

                #Si bon format ajoute le tel dans la bdd avec l'@ de connexion
                else:	
                    msg_serveur = "Ajout du tel"
                    try:
                        ip = self.__socket_client.getsockname()
                        ip = ip[0]
                        conn = sqlite3.connect('bdd_client.sqlite')
                        cur = conn.cursor()
                        cur.execute('SELECT num from Utilisateurs where IP LIKE \'%' + ip + '%\'')
                        res = cur.fetchall()
                        conn.close()
                        try:
                            res = res[0]
                            res = res[0]
                            print(res)
                            print("Le numéro lié est: ", res)
                        except:
                            res = res
                        
                        #Quand l'@IP du client n'est pas encore crée nous l'ajoutons dans la bdd
                        if res == []:
                            print("Utilisateurs pas encore enregistré")
                            #FAIRE LE INSERT 
                            cur.execute("""INSERT Into Utilisateurs (IP,num) VALUES (?,?)""",(ip,msg_client))
                            msg_serveur = 'ajoute'
                            conn.commit()
                            conn.close()
                            fin_echange = True


                        #Quand le champs IP de la base de donné avec l'@ip du client est dejà crée :
                        else:
                            print("Utilisateur déja enregistré ou IP déja utilisé (pas de duplication d'IP)")
                            msg_serveur = 'existant'
                            res = str(res)
                            msg_serveur = msg_serveur + res
                            fin_echange = True

                            print("La connexion SQLite est fermée")


                    except sqlite3.Error as error:
                        print("Erreur lors de la connexion à SQLite", error)

            elif mot_cle == "APL":
                if bonfrormat == False or longeur != 3:
                    msg_serveur = "non existant"
                    fin_echange = True

                #Si bon format ajoute le tel dans la bdd avec l'@ de connexion
                else:	
                    msg_serveur = "non existant"
                    try:
                        msg_client = str(msg_client)
                        conn = sqlite3.connect('bdd_client.sqlite')
                        cur = conn.cursor()
                        print("Base de données crée et correctement connectée à SQLite")
                        cur.execute("""SELECT IP from Utilisateurs where num LIKE ?""",(msg_client,))
                        res = cur.fetchall()
                        conn.close()
                        print(res)
                        try:
                            res = res[0]
                            res = res[0]
                            print(res)
                            print("L'IP appeler est: ", res)
                        except:
                            res = res
                        
                        #Quand l'@IP du client n'est pas encore crée nous l'ajoutons dans la bdd
                        if res == []:
                            print("Utilisateurs pas encore enregistré")
                            msg_serveur = 'non existant'
                            fin_echange = True


                        #Quand le champs IP de la base de donné avec l'@ip du client est dejà crée :
                        else:
                            print("On peut appeler le num")
                            msg_serveur = 'existant: '
                            res = str(res)
                            msg_serveur = msg_serveur + res
                            fin_echange = True


                    except sqlite3.Error as error:
                        print("Erreur lors de la connexion à SQLite", error)
                

            else:
                print("ERRUR mot_clé verifier page connexion")
                msg_serveur = "Pas bon format"
                fin_echange = True

        self.envoyer(msg_serveur)
        return msg_serveur




if __name__ == "__main__":
    # declarations
    port_ecoute: int
    serveurtel: ServeurTel
    # lecture des paramètres du main
    if len(sys.argv) == 2:
        port_ecoute  = int(sys.argv[1])
    else:
        port_ecoute = 5000
    serveurtel = ServeurTel(port_ecoute)
    serveurtel.attenteClient()
