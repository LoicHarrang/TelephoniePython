# ---------------------------------------
# Projet : Téléphonie en Python
# Auteurs : Eliot GUESDON, Mattéo ROBIN, Loic HARRANG
# Fichier : telephone.py
# Objectif : Connecter notre client à son serveur local (RAPPEL : chaque client possède une partie client et une partie serveur)
# ---------------------------------------

from tkinter import *
import socket
import pyaudio
from threading import Thread
from timeit import default_timer



def appel1():
    global CHUNK
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initialisation du modèle TCP
    s.connect(("127.0.0.1", 6000)) # Connection de notre client à son propre serveur local

    thread_ecoute = Thread(target=receive_data) # Déclaration d'un Thread, qui fait référence à la fonction receive_data()
    thread_enregistrer = Thread(target=send_data) # Déclaration d'un Thread, qui fait référence à la fonction send_data()
    
    p = pyaudio.PyAudio()
    connexion = True
    print("Le chat vocal va commencer")

    global receive_stream
    global send_stream
    receive_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    send_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    if connexion == True: # Démarrage et execution des Threads
        thread_ecoute.start()
        thread_enregistrer.start()
        thread_ecoute.join()
        thread_enregistrer.join()



def receive_data():  # Fonction receive_data() qui permet de récuperer et lire des données
    while True:
        try:
            data = s.recv(1024)  # Récupère les données qui transite via le réseau TCP
            print(data)
            receive_stream.write(data)  # Retransmet les données récupéré au dessus dans les haut parleurs de l'ordinateur
        except:
            pass


def send_data():  # Fonction send_data() qui permet d'enregistrer et d'envoyer des données
    while True:
        try:
            data = send_stream.read(CHUNK)  # Enregistre depuis le micro de l'ordinateur
            s.sendall(data)  # Envoie les données enregistré dans le réseau via TCP
            data = send_stream.read(CHUNK)  # Enregistre depuis le micro de l'ordinateur
            s.sendall(data)  # Envoie les données enregistré dans le réseau via TCP
        except:
            pass


class Fen__appel():
    def __init__(self)-> None:
        Tk.__init__(self)

        Toplevel.__init__(self)
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
                


