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

