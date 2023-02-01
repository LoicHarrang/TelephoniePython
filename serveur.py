import socket
from threading import Thread
from socketserver import ThreadingMixIn
import sys
import sqlite3
import select
from tkinter import *


class Fen_Serv(Tk):

    def __init__(self)-> None:
        Tk.__init__(self)
        # déclaration
        self.__lbl_txt: Label
        self.__lbl_value: Label
        self.__btn_actualise: Button

        self.__fen = Frame
        
        # instanciation / initialisation
        self.title("fenetre principale")

        self.geometry("650x500")
        self.resizable(False,False)


        self.__fen = Frame(self, borderwidth=3, relief= "groove",padx=1,pady=1)
        self.__lbl_txt = Label(self.__fen, text="BDD du serveur client et numéro :")
        self.__lbl_value = Label(self.__fen, text="Actualiser une premiere fois")
        self.__btn_actualise = Button(self.__fen,text="Actualiser", command=self.actualiser,width=15)



        # ajout des widgets

        self.__fen.pack(expand=1)
        self.__lbl_txt.pack(pady=1)
        self.__lbl_value.pack(pady = 3)
        self.__btn_actualise.pack(pady=4)
        

    def actualiser(self):
        conn = sqlite3.connect('bdd_client.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * from Utilisateurs')
        res = cur.fetchall()
        self.__lbl_value["text"] = res
        conn.close()


class ServeurTel:
    # constructeur
    def __init__(self, port: int):
        # attributs qui concerne le serveur
        self.__socket_serveur: socket
        self.__port: int = port
        # attributs qui concerne le client
        self.__socket_client: socket
        self.__service: ServiceEchange

        self.__socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

            try:
                variables = msg_client.split(":")
                mot_cle = variables[0]
                longeur = len(variables[1])
                msg_client = int(variables[1])
                bonfrormat = True               

            except:
                bonfrormat = False

            #Renvoie un message au client si pas bon
            if mot_cle == "CHERCHER":
                if bonfrormat == False or longeur != 3:
                    msg_serveur = "Pas bon format"
                    fin_echange = True

                #Si bon format ajoute le tel dans la bdd avec l'@ de connexion
                else:	
                    msg_serveur = "Ajout du tel"
                    try:
                        ip = self.__socket_client.getpeername()
                        ip = ip[0]
                        conn = sqlite3.connect('bdd_client.sqlite')
                        cur = conn.cursor()
                        cur.execute('SELECT num from Utilisateurs where IP LIKE \'%' + ip + '%\'')
                        res = cur.fetchall()
                        try:
                            res = res[0]
                            res = res[0]
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
                            fin_echange = True


                        #Quand le champs IP de la base de donné avec l'@ip du client est dejà crée :
                        else:
                            print("Utilisateur déja enregistré ou IP déja utilisé (pas de duplication d'IP)")
                            msg_serveur = 'existant'
                            res = str(res)
                            msg_serveur = msg_serveur + res
                            fin_echange = True


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
                        print("Connectée BDD SQLite")
                        cur.execute("""SELECT IP from Utilisateurs where num LIKE ?""",(msg_client,))
                        res = cur.fetchall()
                        try:
                            res = res[0]
                            res = res[0]
                            print("L'IP appeler est: ", res)
                        except:
                            res = res
                        
                        #Quand l'@IP du client n'est pas encore crée nous l'ajoutons dans la bdd
                        if res == []:
                            print("Utilisateur pas encore enregistré")
                            msg_serveur = 'non existant'
                            fin_echange = True


                        #Quand le champs IP de la base de donné avec l'@ip du client est dejà crée :
                        else:
                            print("Le numéro est disponible")
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


class Affichage_Serv(Thread):
    def __init__(self):
        Thread.__init__(self)
 
    def run(self):
        self.window=Fen_Serv()
        self.window.mainloop()
 
    def stop(self):
        self.window.destroy()



if __name__ == "__main__":
    # declarations
    port_ecoute: int
    serveurtel: ServeurTel
    # lecture des paramètres du main
    if len(sys.argv) == 2:
        port_ecoute  = int(sys.argv[1])
    else:
        port_ecoute = 5000

#Vider la bdd
    conn = sqlite3.connect('bdd_client.sqlite')
    cur = conn.cursor()
    cur.execute("DELETE FROM 'Utilisateurs'")
    conn.commit()

    affichage=Affichage_Serv()
    affichage.start()
    serveurtel = ServeurTel(port_ecoute)
    serveurtel.attenteClient()
