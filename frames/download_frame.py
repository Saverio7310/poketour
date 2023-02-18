import threading
import concurrent.futures
import customtkinter
import time
from Classes.download import Download
from Database.db_connection import DBConnection

class DownloadFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # variabili collegate ai vari oggetti
        self.var_tour_name = ''
        self.var_tour_code = ''
        self.var_topcut = ''
        self.check_type = 0
        self.check_moveset = 0
        self.check_standing = 0

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
        self.checkbox_type = customtkinter.CTkCheckBox(self, text="Tipologia")
        self.checkbox_type.grid(row=0, column=2, pady=20, padx=20)

        # checkbox per il moveset
        self.checkbox_moveset = customtkinter.CTkCheckBox(self, text="Set mosse")
        self.checkbox_moveset.grid(row=1, column=2, pady=20, padx=20)

        # checkbox che serve a capire se rk9 ha già pubblicato le posizioni finali oppure se 
        # il torneo è ancora in corso e non bisogna salvare le posizioni 
        self.checkbox_standing = customtkinter.CTkCheckBox(self, text="Posizioni pubblicate")
        self.checkbox_standing.grid(row=2, column=2, pady=20, padx=20)

        # bottone per confermare
        self.confirm_choices_button = customtkinter.CTkButton(self, command=self.confirm_button_event,
                                                              text='Conferma')
        self.confirm_choices_button.grid(row=3, column=2, padx=20, pady=10)


    # funzine che controlla se i campi necessari del central frame sono presenti
    def check_missing_attributes(self):
        self.var_tour_name = self.entry_tour_name.get().strip()
        self.var_tour_code = self.entry_tour_code.get().strip()
        self.var_topcut = self.optionmenu.get()
        self.check_type = self.checkbox_type.get()
        self.check_moveset = self.checkbox_moveset.get()
        self.check_standing = self.checkbox_standing.get()
        if self.var_tour_name == '' or self.var_tour_code == '':
            raise Exception('Nome o codice torneo mancante!')
        
    # funzione che permette il download dei dati tramite connessione internet
    def download_data(self, start):
        down = Download()
        try:
            table = down.establish_connection(code=self.var_tour_code)
        except Exception as exp:
            print(exp)
            return
        
        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')

        list_all_teams_link = down.get_teams_link(table=table)
        print('Ho preso i link')

        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')

        list_of_pokemon_tuple = list()

        try:
            # creo 8 thread invece del massimo (sul mio pc 12) per evitare di intasare il server che
            # potrebbe chiudere la connessione
            with concurrent.futures.ThreadPoolExecutor(8) as executor:
                results = executor.map(down.get_table_html, list_all_teams_link)

            for result in results:
                list_of_pokemon_tuple += down.get_all_teams(result)

        except ValueError:
            raise ValueError
        except Exception:
            raise Exception

        #list_of_tuple = down.get_all_teams(teams_link=list_all_teams_link)
        print(len(list_of_pokemon_tuple))
        print(list_of_pokemon_tuple[0])
        print('Ho preso i pokemon')

        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')

        return (list_all_teams_link, list_of_pokemon_tuple)

    # funzione che permette il salvataggio dei dati creando la connessione al db
    def save_data(self, db, conn, start, list_all_teams_link, list_of_pokemon_tuple):
        

        print('Creo la tabella')
        db.create_table_new_tournament(conn, self.var_tour_code)

        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')

        print('Inserisco il torneo nella tabella tornei')
        db.insert_tournament(conn, self.var_tour_name, self.var_tour_code)

        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')

        # mi servono solo i codici, non tutto il link, quindi devo ricavarmelo
        list_link_standing = [(link[-20:], stand) for link, stand in list_all_teams_link]

        print('Inserisco i link nella tabella del torneo')
        db.insert_links(conn, self.var_tour_code, list_link_standing)

        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')

        print('Inserisco i pokemon nella tebella dei team')
        db.insert_pokemons(conn, self.var_tour_code, list_of_pokemon_tuple)

        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')

        db.close_connection(conn)
        print('Ho chiuso la connessione con il db')

        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')

    # funzione che fa partire il download dei dati ed il salvataggio nel db
    def start_downloading_and_saving(self):
        try:
            self.check_missing_attributes()
        except Exception as exp:
            print(exp)
            return
        
        start = time.perf_counter()

        db = DBConnection()
        print('Inizio la connessione al db')
        conn = db.start_connection()

        finish = time.perf_counter()
        print(f'Finito in {round(finish-start, 2)} secondi')
        
        result = db.check_already_saved_tournament(conn, self.var_tour_code)

        if result[0]:
            print('Il torneo è già stato salvato', result[0])
            return

        
        self.confirm_choices_button.configure(state='disabled')

        try:
            list_all_teams_link, list_of_pokemon_tuple = self.download_data(start)
        except ValueError:
            print('Le teamlist non sono state ancora pubblicate')
            self.confirm_choices_button.configure(state='normal')
            return
        except Exception:
            print('Errore di comunicazione tra applicazione e server!')
            self.confirm_choices_button.configure(state='normal')
            return

        self.save_data(db, conn, start, list_all_teams_link, list_of_pokemon_tuple)
        
        self.confirm_choices_button.configure(state='normal')
        '''
        '''

    # funzione che viene chiamata quando si preme il tasto 'Conferma'
    def confirm_button_event(self):
        # si usa un thread per evitare che l'intera applicazione si blocchi per aspettare che la 
        # funzione chiamata finisca
        threading.Thread(target=self.start_downloading_and_saving).start()