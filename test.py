from tkinter import *



class Fen_Principale(Tk):

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
        self.__lbl_txt = Label(self.__fen, text="BDD du serveur :")
        self.__lbl_value = Label(self.__fen, text="Actualiser une premiere fois")
        self.__btn_actualise = Button(self.__fen,text="Actualiser", command=self.actualiser,width=15)



        # ajout des widgets

        self.__fen.pack(expand=1)
        self.__lbl_txt.pack(pady=1)
        self.__lbl_value.pack(pady = 3)
        self.__btn_actualise.pack(pady=4)
        

    def actualiser(self):
        pass

tqt = Fen_Principale()
tqt.mainloop()