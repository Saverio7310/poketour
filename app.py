'''
quando nel grid si usa nsew si intende north south east west, ovvero le direzioni in cui si deve espandere. Si può
usare una qualsiasi combinazione di queste quattro lettere.
padx e pady indicano lo spazio che si deve lasciare dal bordo massimo. padx => (da destra, da sinistra)
pady => (da sopra, da sotto).
rowspan e columnspand indicano quanto un oggetto può espandersi rispettivamente su più righe e più colonne.

Se in un frame voglio cvhe gli oggetti siano equidistanti anche quando modifico la grandezza di una finestra devo 
usare il grid_row/columnfigure, che dice all'app se le righe e le colonne possono o meno cambiare dimensione. Se
assieme uso sticky='nsew' allora oltre a muoversi gli elementi andranno ad occupare tutto lo spazio possibile
'''

import tkinter
import customtkinter
import Frames.sidebar_frame as sf
import Frames.central_frame as cf

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Analisi tornei")
        self.geometry(f"{1000}x{800}")
        self.minsize(800, 600)

        # configure grid layout (2x2)
        # con valore 0 una riga non si espande in verticale
        # con valore 0 una colonna non si espande in orizzontale 
        #self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        #self.grid_columnconfigure(0, weight=1)

        # menu interno dell'app
        self.menu_bar = tkinter.Menu(self)
        self.config(menu=self.menu_bar)

        # funzioni associate ai menu
        self.sidebar_frame_visible = False
        def show_tournaments():
            if not self.sidebar_frame_visible:
                self.central_frame.grid(row=0, column=1)
                self.sidebar_frame.grid(row=0, column=0, sticky='nws', padx=10, pady=10)
                self.sidebar_frame.grid_propagate(0)
                self.sidebar_frame.configure(width=300)
                self.sidebar_frame_visible = True
            else:
                self.sidebar_frame.grid_forget()
                self.central_frame.grid(row=0, column=0)
                self.sidebar_frame_visible = False

        # menu dei file
        self.file_menu = tkinter.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Mostra Tornei', command=show_tournaments)



        # frame della sidebar
        self.sidebar_frame = sf.SidebarFrame(self, corner_radius=10)
        

        # frame centrale per l'inserimento dei dati
        self.central_frame = cf.CentralFrame(self, corner_radius=10)
        self.central_frame.grid(row=0, column=0, columnspan = 2, sticky='nsew', padx=10, pady=10)
        self.central_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.central_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # textbox in basso
        self.textbox = customtkinter.CTkTextbox(self, corner_radius=10)
        #self.textbox.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")




    # funzioni associate agli oggetti

    '''
    OCpGIIa9m9BGzlZ8B5Gt
    h7kIYruNMePQMy4UZkMj
    '''

if __name__ == "__main__":
    app = App()
    app.mainloop()