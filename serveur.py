import socket
import sys 

class ServiceEcoute:
    def __init__(self, port_serveur: int)-> None:
        self.__socket_ecoute : socket = None
        self.__port_ecoute : int = port_serveur
        self.__socket_ecoute = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_ecoute.bind(("",self.__port_ecoute))
        # mise en ecoute avec le nombre de connexion simultanées possibles
        self.__socket_ecoute.listen(1)
        print(f"serveur en ecoute sur le port {self.__port_ecoute} ...")



    def attente(self)-> socket: 

        # attente d'une demande de connexion
        socket_echange, ADDR = self.__socket_ecoute.accept() # bloquante
        # fermeture de l'ecoute (ici gestion d'un seul client)
        print("une nouvelle demande de connexion")
        # affichage des information de la machine distante
        print(f"sochet echange : {socket_echange}")
        print(f"adr : {ADDR}")
        return socket_echange



class ServiceEchange:
    def __init__(self, socket_echange: socket)-> None: 
        self.__socket_echange : socket = socket_echange


    def envoyer(self, msg: str)-> None:
        tab_bytes = msg.encode("utf-8")
        self.__socket_echange.send(tab_bytes)

    def recevoir(self)-> str: 
        tab_bytes = self.__socket_echange.recv(255)
        res = tab_bytes.decode("utf-8")
        return res 

    def echange(self)->None:
        fin : bool = False
        while(not fin):
            # mise en forme et affichage du message du client
            recu = self.recevoir()
            # preparation de la réponse
            if recu == "fin":
                fin = True
            print(f"C => S: {recu}")
            # envoi de la réponse
            msg_server = f"[{recu}]"
            self.envoyer({msg_server})

    

    def arret(self)-> None:
        print(f"Connexion fermée")
        self.__socket_echange.close()



if __name__ == "__main__":
    # declaration des variables
    port_ecoute: int = None
    service_ecoute: ServiceEcoute = None
    socket_client: socket = None
    service_echange: ServiceEchange = None
    # lecture des parametres (le numero de port)
    if len(sys.argv) >= 2:
        port_ecoute = int(sys.argv[1])
    else:
        port_ecoute = 5000
    
    service_ecoute = ServiceEcoute(port_ecoute)
    socket_client = service_ecoute.attente()
    service_echange = ServiceEchange(socket_client)
    service_echange.echange()
    