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

class Fen_appel(Toplevel):

    def __init__(self, fp: Fen_Principale)-> None:

        Toplevel.__init__(self)
        self.__fp = fp
        self.__fp.withdraw()
        self.title("fenetree")

        self.geometry("650x500")
        self.resizable(False,False)
        #self.backgroundImage=PhotoImage(file="wallpaper.png")
        #self.backgroundImageLabel = Label(self,image = self.backgroundImage)
        #self.backgroundImageLabel.place(x=0,y=0)
        self.canva = Canvas(self)
        self.canva.pack(padx=10,pady=10)

        def updateTime():
            now = default_timer() - start
            minutes, seconds = divmod(now, 60)
            hours, minutes = divmod(minutes, 60)
            str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
            self.canva.itemconfigure(text_clock, text=str_time)
            self.after(1000, updateTime)

        self.__fen = Frame(self, borderwidth=3, relief= "groove", padx=10, pady=10)
        start = default_timer()
        text_clock = self.canva.create_text(193,40,justify='center', font = 'Helvetica 16')

        updateTime()

        self.__fen.pack(expand=1)


if __name__ == "__main__":
    bite = Fen_appel()
    bite.mainloop()