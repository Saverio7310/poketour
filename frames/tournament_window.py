import customtkinter
import tkinter
from tkinter import ttk
from Database.db_connection import DBConnection

class TournamentWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, tour_name='Nome Torneo', tour_code='Codice Torneo',  **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("800x600")
        self.title('Analisi ' + str(tour_name))

        self.label_name = customtkinter.CTkLabel(self, text=tour_name)
        self.label_name.grid(padx=20, pady=20)

        db = DBConnection()
        conn = db.start_connection()
        participants, top_poke, top_tera = db.get_general_info(conn, tour_code)

        self.frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        columns = ('name', 'usage')

        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        self.tree.grid(row=1, column=0, sticky='nsew')

        self.tree.heading('name', text='Name')
        self.tree.heading('usage', text='Usage')

        for tup in top_poke:
            self.tree.insert('', tkinter.END, values=tup)

        self.label_part = customtkinter.CTkLabel(self.frame, text=participants)
        self.label_part.grid(row=0, column=0, sticky='nsew')

        '''
        for tup in top_poke:
            self.label_top_poke = customtkinter.CTkLabel(self.frame, text=tup)
            self.label_top_poke.grid(padx=20, pady=20)

        for tup in top_tera:
            self.label_top_tera = customtkinter.CTkLabel(self.frame, text=tup)
            self.label_top_tera.grid(padx=20, pady=20)
        '''



