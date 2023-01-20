from tkinter import *
import socket
import pyaudio
from threading import Thread
from connexion import ClientTel
from telephone import appel1
import select
from tkinter import messagebox
import time
from timeit import default_timer



class Fen_Principale(Tk):

    def __init__(self)-> None:
        Tk.__init__(self)
        # déclaration

        self.__lbl_adr_port: Label
        self.__adr_port_init: str
        self.__btn_config: Button
        self.__btn_init: Button
        self.__btn_quitter: Button
        self.__fen = Frame
        
        # instanciation / initialisation
        self.title("fenetre principale")

        self.geometry("650x500")
        self.resizable(False,False)
        self.backgroundImage=PhotoImage(file="wallpaper.png")
        self.backgroundImageLabel = Label(self,image = self.backgroundImage)
        self.backgroundImageLabel.place(x=0,y=0)

        self.__fen = Frame(self, borderwidth=3, relief= "groove",padx=1,pady=1)
        self.__adr_port_init = "ADRESSE DU SERVEUR : xxx.xxx.xxx.xxx : xxx"
        self.__lbl_adr_port = Label(self.__fen, text=self.__adr_port_init)
        self.__btn_config = Button(self.__fen, text= "CONFIGURATION", command = lambda: Fen_Config(self), width=15)
        self.__btn_init = Button(self.__fen, text= "CONNEXION", width=15, command=self.connexion)
        self.__btn_quitter = Button(self.__fen, text= "QUITTER", bg="red", command= self.destroy)
        self.__lbl_tel = Label(self.__fen, text="Ton numéro de téléphone est :", width=25)
        self.__ent_tel = Entry(self.__fen,width=5,state=DISABLED)
        self.__btn_tel = Button(self.__fen,text="Choix", command=self.authentification,state=DISABLED)
        self.__lbl_erreur = Label(self.__fen, text="Il faut respecter 3 chiffres pour ton numéro", width=40)

        self.__lbl_apll = Label(self.__fen, text="Tu veux appeler :", width=25)
        self.__ent_apll = Entry(self.__fen,width=5,state=DISABLED)
        self.__btn_apll = Button(self.__fen,text="Choix", command = self.appeler, state=DISABLED)
        self.__lbl_appll2 = Label(self.__fen, text="Numéro destinataire 3 chiffres", width=40)


        # ajout des widgets

        self.__fen.pack(expand=1)
        self.__lbl_adr_port.pack(pady=1)
        self.__btn_config.pack(pady = 3)
        self.__btn_init.pack(pady=3)
        
        self.__fen.pack(expand=	1)
        self.__lbl_tel.pack(pady=1,padx=0)
        self.__ent_tel.pack(pady=1,padx=1)
        self.__btn_tel.pack(pady=3)
        self.__lbl_erreur.pack(pady=4)

                
        self.__lbl_apll.pack(pady=1,padx=0)
        self.__ent_apll.pack(pady=1,padx=1)
        self.__btn_apll.pack(pady=3)
        self.__lbl_appll2.pack(pady=4)
        self.__btn_quitter.pack(pady=5)



    #modificateurs

    def set_lbl_adr_port(self, chaine: str)-> None:
        self.__lbl_adr_port["text"] = chaine
        print(chaine)

    def init(self)-> None:
        self.__lbl_adr_port["text"] = self.__adr_port_init

    def get_ip_port(self)->str:
        return self.__lbl_adr_port["text"]


    def connexion(self):
        ipport = self.__lbl_adr_port["text"]

        try:
            ipport = ipport.split(':')
            self.__ipserveur = ipport[1].lstrip()
            self.__portserveur = int(ipport[2].lstrip())
            self.__portserveur = int(self.__portserveur)
            self.__Client = ClientTel(self.__ipserveur,self.__portserveur)
            connexion_ok = self.__Client.get_connexion()
            if connexion_ok : 
                self.__btn_config["state"] = DISABLED
                self.__btn_init["state"] = DISABLED
                self.__btn_tel["state"] = NORMAL
                self.__ent_tel["state"] = NORMAL

            
        except:
            pass

    def authentification(self):
        tel : str = ""
        try:
            self.__Client = ClientTel(self.__ipserveur,self.__portserveur)
            num = self.__ent_tel.get()
            tel = self.__Client.enregistrement(num)

            if tel == "Pas bon format":
                self.__lbl_erreur.config(fg="red")
                print("Mauvais format")

            else:
                if tel == "ajoute":
                    self.__btn_tel["state"] = DISABLED 
                    self.__ent_tel["state"] = DISABLED
                    self.__btn_apll["state"] = NORMAL
                    self.__ent_apll["state"] = NORMAL
                    self.__lbl_erreur.config(fg="black")
                    self.__lbl_erreur["text"]="Votre numéro est enregistré"
                    print("Bon format et enregistré")

                else:
                    existant : str = "Votre IP est déja associé au numéro : "
                    num = tel[-3:]
                    self.__lbl_erreur["fg"]="red"
                    existant = existant + num
                    self.__lbl_erreur.config(text=existant)
                    self.__btn_tel["state"] = DISABLED 
                    self.__ent_tel["state"] = DISABLED
                    self.__btn_apll["state"] = NORMAL
                    self.__ent_apll["state"] = NORMAL
        except:
            pass


    def appeler(self):
        self.__Client = ClientTel(self.__ipserveur,self.__portserveur)
        qui_appeler = self.__ent_apll.get()
        ip_destinataire = self.__Client.destinataire(qui_appeler)
        if ip_destinataire == "non existant":
            self.__lbl_appll2["fg"]="red"
            self.__lbl_appll2["text"]="Vous devez joindre un numéro existant"
            print("Pas existant")

        else:
            self.__btn_apll["state"] = DISABLED
            ip_destinataire = ip_destinataire.split(":")
            ip_destinataire = ip_destinataire[1]
            ip_destinataire.replace(" ","")
            print("Pour appeler vous aller communiquer avec l'ip :",ip_destinataire)
            self.__lbl_appll2["fg"]="black"
            self.__lbl_appll2["text"] ="Appel en cours"
            appel(ip_destinataire)
            self.__btn_apll["state"] = NORMAL

def appel(ip):
    global CHUNK
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    ip = ip.split()
    ip = ip[0]

    global s
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
    
    elif connexion == True and connects == True:
        thread_ecoute.start()
        thread_enregistrer.start()
        thread_ecoute.join()
        thread_enregistrer.join()

    
connects : bool = False
def receive_data():
    while True:
        try:
            data = s.recv(1024)
            print(data)
            if data != "":
                global connects
                connects = True
                receive_stream.write(data)
                print(connects)
                
            else :
                pass

        except:
            pass

def send_data():
    while True:
        try:
            data = send_stream.read(CHUNK)
            s.sendall(data)
        except:
            pass
                

class Fen_Config(Toplevel):

    def __init__(self, fp: Fen_Principale)-> None:

        Toplevel.__init__(self)
        self.__fp = fp

        # declaration

        self.__lbl_adr: Label
        self.__entree_adr: Entry
        self.__lbl_port: Label
        self.__entree_port: Entry
        self.__btn_retour: Button
        self.__fen = Frame

        # instantiation / initialisation

        self.__fp.withdraw()
        self.title("config")

        self.geometry("650x500")
        self.resizable(False,False)
        self.backgroundImage=PhotoImage(file="wallpaper.png")
        self.backgroundImageLabel = Label(self,image = self.backgroundImage)
        self.backgroundImageLabel.place(x=0,y=0)

        self.__fen = Frame(self, borderwidth=3, relief= "groove", padx=10, pady=10)
        self.__lbl_adr = Label(self.__fen, text= "ADRESSE SERVEUR")
        self.__entree_adr = Entry(self.__fen, width= 15)
        self.__entree_adr.insert(0, "127.0.0.1")
        self.__lbl_port = Label(self.__fen, text= "PORT SERVEUR")
        self.__entree_port = Entry(self.__fen, width= 5)
        self.__entree_port.insert(0, "5000")
        self.__btn_retour = Button(self.__fen, text= "VALIDER", command= self.configuration)

        # ajout des widgets
        
        self.__fen.pack(expand=1)
        self.__lbl_adr.grid(row= 0, column= 0)
        self.__entree_adr.grid(row= 0, column= 1)
        self.__lbl_port.grid(row= 1, column= 0)
        self.__entree_port.grid(row= 1, column= 1)
        self.__btn_retour.grid(row= 2, column=0)
        self.protocol("WM_DELETE_WINDOW", self.configuration)

    def configuration(self)-> None:
        adr_port: str = f"ADRESSE DU SERVEUR : {self.__entree_adr.get()} : {self.__entree_port.get()}"
        self.__fp.set_lbl_adr_port (adr_port)
        self.__fp.deiconify() # afficher la fenetre 
        self.destroy() #detruire la fenetre courante

    def get_socket(self)-> float:
        self.socket_appel : float = f'"{self.__entree_adr.get()}",{self.__entree_port.get()}'
        return self.socket_appel




class Fen_jsuisappel(Toplevel):
    def __init__(self, fp: Fen_Principale,num)-> None:
        Toplevel.__init__(self)

        self.__fp = fp
        # déclaration
        self.title("j apelle")

        self.__fen : Frame
        self.__btn_accept: Button
        self.__btn_refuse : Button
        
        self.__fen = Frame(self,borderwidth=3, relief= "groove",padx=20,pady=20)
        self.__lbl_appelarrive = Label(self.__fen,text=f"Un appel en provenance de : {num} ")
        self.__btn_accept = Button(self.__fen,text = "Accepter", bg="green", command=self.appel)
        self.__btn_refuse = Button(self.__fen,text="Refuser",bg ="red", command=self.detruire)

        #Affichage dans le tk
        self.__fen.pack(expand=0)
        self.__lbl_appelarrive.grid(row=1, column=0)
        self.__btn_accept.grid(row=2, column=0)
        self.__btn_refuse.grid(row=2, column=1)


    def appel(self):
        appelencours()
        self.destroy()


    def detruire(self):
        destroy()
        self.destroy()


accept_appel = False
def appelencours():
    print("Appel ok")
    global accept_appel 
    accept_appel = True
    print(accept_appel)


def destroy():
    print("Appel pas ok")
    global accept_appel 
    global fermeture_port
    accept_appel = False
    fermeture_port = True


class Fen_appel(Toplevel):

    def __init__(self, fp: Fen_Principale)-> None:

        Toplevel.__init__(self)
        self.__fp = fp
        self.title("fenetre appel")

        self.geometry("400x300")
        self.resizable(False,False)
        self.backgroundImage=PhotoImage(file="wallpaper.png")
        self.backgroundImageLabel = Label(self,image = self.backgroundImage)
        self.backgroundImageLabel.place(x=0,y=0)
        self.canva = Canvas(self, width = 300, height = 400)
        self.canva.pack(padx=10,pady=10)
        self.__btn_raccrocher: Button

        self.__btn_raccrocher = Button(self.canva, text= "RACCROCHER", width=15, bg="red", command=self.raccrocher)

        def updateTime():
            now = default_timer() - start
            minutes, seconds = divmod(now, 60)
            hours, minutes = divmod(minutes, 60)
            str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
            self.canva.itemconfigure(text_clock, text=str_time)
            self.after(1000, updateTime)

        self.__fen = Frame(self, borderwidth=3, relief= "groove", padx=10, pady=10)
        start = default_timer()
        text_clock = self.canva.create_text(155,40,justify='center', font = 'Helvetica 24')

        updateTime()

        self.canva.create_window(153,225, window=self.__btn_raccrocher)

    def raccrocher(self):
        self.destroy()
        raccroche()

def raccroche():
    global fermeture_port
    global accept_appel
    accept_appel = False
    fermeture_port = True
        

class ChatServer:
    def __init__(self):
        self.CONNECTION_LIST = []
        self.chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_adress = ('127.0.0.1',6000)
        self.chat_server_socket.bind(serv_adress)
        print("ecoute commence")

    def run(self):
        global fermeture_port
        fermeture_port = False
        global apparaitre
        apparaitre = False
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

        while True:
            try:
                if accept_appel == True and apparaitre == False:
                    apparaitre = True
                    Fen_appel(self)


                elif accept_appel == True and apparaitre == True:
                    recevoir, addresse = self.chat_server_socket.recvfrom(1024)
                    stream.write(recevoir)
                    envoie = stream.read(1024)
                    self.chat_server_socket.sendto(envoie,addresse)


                else:
                    pass

            except socket.error:
                print("left the server")
                self.chat_server_socket.close()
                self.CONNECTION_LIST.remove(self.chat_server_socket)

            if fermeture_port == True:
                self.chat_server_socket.close()
                fermeture_port = False
            else:
                pass

            self.chat_server_socket.close()
            p.terminate()

        


class Affichage(Thread):
    def __init__(self):
        Thread.__init__(self)
 
    def run(self):
        self.window=Fen_Principale()
        self.window.mainloop()
 
    def stop(self):
        self.window.destroy()

class Tel(Thread):
    def __init__(self):
        Thread.__init__(self)
 
    def run(self):
        ChatServer().run()

"""
class Tel1(Thread):
    def __init__(self):
        Thread.__init__(self)
 
    def run(self):
        appel1()
"""


if __name__ == "__main__":

    try:
        affichage=Affichage()
        affichage.start()
        ecoutetel = Tel()
        ecoutetel.start()
        """
        try:
            tel = Tel1()
            tel.start()
        except:
            pass
        """
    except:
        print("erreur dans le programme")


"""
            rlist, wlist, xlist = select.select(self.CONNECTION_LIST, [], [])
            for current_socket in rlist:
                if current_socket is self.chat_server_socket and len(self.CONNECTION_LIST) < 3 :
                    (new_socket, address) = self.chat_server_socket.accept()
                    self.CONNECTION_LIST.append(new_socket)
                    print("connected to the server")
                    
                else:

                    if accept_appel != True and len(self.CONNECTION_LIST) > 2:
                    ip = self.CONNECTION_LIST[2]
                    ip = ip.getpeername()
                    ip = ip[0]
                    Fen_jsuisappel(self,ip)
                    while fermeture_port == False and accept_appel == False:
                        time.sleep(0.001)

            """