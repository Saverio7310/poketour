import tkinter
import customtkinter
from Classes.download import Download
from Database.db_connection import DBConnection

class CentralFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # variabili collegate ai vari oggetti
        self.check_type = tkinter.IntVar()

        # entry per il nome del torneo
        self.label_tour_name = customtkinter.CTkLabel(self, width=200, text="Nome torneo", anchor='w')
        self.label_tour_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_tour_name = customtkinter.CTkEntry(self, width=200, placeholder_text="es. Orlando 2023")
        self.entry_tour_name.grid(row=0, column=1, padx=10, pady=10, columnspan=1)

        # entry per il codice del torneo
        self.label_tour_code = customtkinter.CTkLabel(self, width=200, text="Codice rk9 del torneo", anchor='w')
        self.label_tour_code.grid(row=1, column=0, padx=10, pady=10)
        self.entry_tour_code = customtkinter.CTkEntry(self, width=200, placeholder_text="es. h7kIYruNMePQMy4UZkMj")
        self.entry_tour_code.grid(row=1, column=1, padx=10, pady=10)

        # optionmenu per la scelta della top da analizzare 
        self.label_topcut = customtkinter.CTkLabel(self, width=200, text="Partecipanti", anchor='w')
        self.label_topcut.grid(row=2, column=0, padx=10, pady=10)
        self.optionmenu = customtkinter.CTkOptionMenu(self, width=200, dynamic_resizing=False,
                                                        values=["Top 32", "Top 64", "Top 128", "All"])
        self.optionmenu.grid(row=2, column=1, padx=10, pady=10)

        # checkbox per la tipologia
        self.checkbox_type = customtkinter.CTkCheckBox(self, text="Tipologia", variable=self.check_type)
        self.checkbox_type.grid(row=0, column=2, pady=20, padx=20)

        # checkbox per il moveset
        self.checkbox_type = customtkinter.CTkCheckBox(self, text="Set mosse")
        self.checkbox_type.grid(row=1, column=2, pady=20, padx=20)

        # checkbox che serve a capire se rk9 ha già pubblicato le posizioni finali oppure se 
        # il torneo è ancora in corso e non bisogna salvare le posizioni 
        self.checkbox_standing = customtkinter.CTkCheckBox(self, text="Posizioni pubblicate")
        self.checkbox_standing.grid(row=2, column=2, pady=20, padx=20)

        # bottone per confermare
        self.confirm_choices_button = customtkinter.CTkButton(self, command=self.confirm_button_event,
                                                              text='Conferma')
        self.confirm_choices_button.grid(row=3, column=2, padx=20, pady=10)


    def confirm_button_event(self):
        print(self.check_type.get())
        down = Download()
        '''
        '''
        db = DBConnection()
        cursor = db.start_connection()
        result = db.exec_tables_creation(cursor)
        print(result)
        