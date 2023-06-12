import threading
import concurrent.futures
import customtkinter
import time
import re
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

        # label + entry per il nome del torneo
        self.label_tour_name = customtkinter.CTkLabel(self, text="Nome torneo", anchor='w')
        self.label_tour_name.grid(row=0, column=0, padx=10, pady=10, sticky = 'ew')
        self.entry_tour_name = customtkinter.CTkEntry(self, placeholder_text="es. Orlando")
        self.entry_tour_name.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky = 'ew')

        # label + entry per il codice del torneo
        self.label_tour_code = customtkinter.CTkLabel(self, text="Codice rk9 del torneo", anchor='w')
        self.label_tour_code.grid(row=1, column=0, padx=10, pady=10, sticky = 'ew')
        self.entry_tour_code = customtkinter.CTkEntry(self, placeholder_text="es. h7kIYruNMePQMy4UZkMj")
        self.entry_tour_code.grid(row=1, column=1, padx=10, pady=10, columnspan = 2, sticky = 'ew')

        # progressbar che indica il copmletamento del download
        self.progressbar = customtkinter.CTkProgressBar(self)
        self.progressbar.configure(mode="indeterminate")

        # label che da indicazioni sul completamento dei dati
        self.label_message = customtkinter.CTkLabel(self, justify='left', anchor='w')
        message = 'Il procedimento potrebbe richiedere alcuni minuti\nin base al numero di partecipanti!'
        self.label_message.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.label_message.configure(text = message)
        self.label_message.grid_propagate(0)

        """ # optionmenu per la scelta della top da analizzare 
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
        self.checkbox_standing.grid(row=2, column=2, pady=20, padx=20) """

        # bottone per confermare
        self.confirm_choices_button = customtkinter.CTkButton(self, command=self.confirm_button_event,
                                                              text='Conferma')
        self.confirm_choices_button.grid(row=2, column=0, padx=20, pady=10, sticky='w')


    # funzine che controlla se i campi necessari del central frame sono presenti
    def check_missing_attributes(self):
        self.var_tour_name = self.entry_tour_name.get().strip()
        self.var_tour_code = self.entry_tour_code.get().strip()
        """ self.var_topcut = self.optionmenu.get()
        self.check_type = self.checkbox_type.get()
        self.check_moveset = self.checkbox_moveset.get()
        self.check_standing = self.checkbox_standing.get() """
        if self.var_tour_name == '' or self.var_tour_code == '':
            raise Exception('Nome o codice torneo mancante!')
        result = re.search('\W', self.var_tour_code)
        if result:
            raise Exception('Non sono ammessi caratteri speciali!')

        if len(self.var_tour_code) != 20:
            raise Exception('Lunghezza codice errata, inserire 20 caratteri!')
        
    # funzione che permette il download dei dati tramite connessione internet
    def download_data(self, start):
        down = Download()
        self.label_message.configure(text = 'Connessione al sito.')
        try:
            table = down.establish_connection(code=self.var_tour_code)
        except Exception as exp:
            raise Exception(exp)
        
        finish = time.perf_counter()
        print(f'Connessione effettuata in {round(finish-start, 2)} secondi')

        self.label_message.configure(text = 'Connessione alle pagine dei team.')
        try:
            list_all_teams_link = down.get_teams_link(table=table)
        except ValueError as exp:
            print('Eccezione lanciata dalla funzione get tams link')
            raise ValueError(exp)

        finish = time.perf_counter()
        print(f'Link dei team salvati in {round(finish-start, 2)} secondi')

        list_of_pokemon_tuple = list()

        # scelta del numero di thread per il downloa dei dati. Maggiore è il numero di link a cui accedere
        # minore sarà il numero di thread da utilizzare per evitare di intasare il sito che potrebbe 
        # chiudere la connessione
        teams_number = len(list_all_teams_link)
        if teams_number >= 300 and teams_number < 800:
            thread_number = 10 - teams_number//100
        elif teams_number < 300:
            thread_number = 8
        elif teams_number >= 800:
            thread_number = 2

        self.label_message.configure(text = 'Download dei dati.')

        try:
            # creo n thread invece del massimo (sul mio pc 12) per evitare di intasare il server che
            # potrebbe chiudere la connessione
            with concurrent.futures.ThreadPoolExecutor(thread_number) as executor:
                results = executor.map(down.get_table_html, list_all_teams_link)

            for result in results:
                list_of_pokemon_tuple += down.get_all_teams(result)

        except ValueError as exp:
            print('Eccezione lanciata dal try except del thread pool excecutor')
            raise ValueError(exp)
        except Exception as exp:
            raise Exception(exp)

        #list_of_tuple = down.get_all_teams(teams_link=list_all_teams_link)
        print(len(list_of_pokemon_tuple))
        print(list_of_pokemon_tuple[0])

        finish = time.perf_counter()
        print(f'Salvataggio Pokemon avvenuto in {round(finish-start, 2)} secondi')

        self.label_message.configure(text = 'Download concluso, inizio salvataggio dati.')

        return (list_all_teams_link, list_of_pokemon_tuple)

    # funzione che permette il salvataggio dei dati creando la connessione al db
    def save_data(self, db, conn, start, list_all_teams_link, list_of_pokemon_tuple):

        db.create_table_new_tournament(conn, self.var_tour_code)

        finish = time.perf_counter()
        print(f'Creazione tabelle in {round(finish-start, 2)} secondi')

        db.insert_tournament(conn, self.var_tour_name, self.var_tour_code)

        finish = time.perf_counter()
        print(f'Inserimento torneo in {round(finish-start, 2)} secondi')

        # mi servono solo i codici, non tutto il link, quindi devo ricavarmelo
        list_link_standing = [(link[-20:], stand) for link, stand in list_all_teams_link]

        db.insert_links(conn, self.var_tour_code, list_link_standing)

        finish = time.perf_counter()
        print(f'Inserisco i link nella tabella in {round(finish-start, 2)} secondi')

        db.insert_pokemons(conn, self.var_tour_code, list_of_pokemon_tuple)

        finish = time.perf_counter()
        print(f'Pokemon inseirti nella tabella dei team in {round(finish-start, 2)} secondi')

        db.close_connection(conn)
        print('Ho chiuso la connessione con il db')

        finish = time.perf_counter()
        print(f'Chiusura database e terminazione delle operazioni dopo {round(finish-start, 2)} secondi')

    # funzione che fa partire il download dei dati ed il salvataggio nel db
    def start_downloading_and_saving(self):
        try:
            self.check_missing_attributes()
        except Exception as exp:
            # mostro il label con il messaggio di errore e dopo 3 secondi scompare automaticamente
            #self.label_message.grid(row=2, column=1, padx=10, pady=10, sticky='nse')
            self.label_message.configure(text = exp)
            self.after(3000, lambda : self.label_message.grid_forget())
            return
        
        start = time.perf_counter()

        db = DBConnection()
        conn = db.start_connection()

        finish = time.perf_counter()
        print(f'Connessione al database effettuata in {round(finish-start, 2)} secondi')
        
        result = db.check_already_saved_tournament(conn, self.var_tour_code)

        if result[0]:
            # mostro il label con il messaggio di errore e dopo 3 secondi scompare automaticamente
            #self.label_message.grid(row=2, column=1, padx=10, pady=10, sticky='nse')
            self.label_message.configure(text = 'Il torneo è già stato salvato')
            self.after(3000, lambda : self.label_message.grid_forget())
            return
        
        # inizio delle operazioni, messaggio di inizio viene mostrato
        self.confirm_choices_button.configure(state='disabled')
        #self.label_message.grid(row=2, column=1, padx=10, pady=10, sticky='nse')
        self.label_message.configure(text = 'Inizio download dei dati!')
        self.progressbar.grid(row=3, column=1, padx=10, pady=10, sticky="new")
        self.progressbar.start()

        # inizio del download dei dati con la funzione definita sopra
        try:
            list_all_teams_link, list_of_pokemon_tuple = self.download_data(start)
        except ValueError as exp:
            # mostro il label con il messaggio di errore e dopo 3 secondi scompare automaticamente
            #self.label_message.grid(row=2, column=1, padx=10, pady=10, sticky='nse')
            self.label_message.configure(text = exp)
            self.after(3000, lambda : self.label_message.grid_forget())
            self.progressbar.grid_forget()
            self.confirm_choices_button.configure(state='normal')
            return
        except Exception as exp:
            # mostro il label con il messaggio di errore e dopo 3 secondi scompare automaticamente
            #self.label_message.grid(row=2, column=1, padx=10, pady=10, sticky='nse')
            self.label_message.configure(text = exp)
            self.after(3000, lambda : self.label_message.grid_forget())
            self.progressbar.grid_forget()
            self.confirm_choices_button.configure(state='normal')
            return

        # inizio del salvataggio dei dati con la funzione definita sopra
        self.save_data(db, conn, start, list_all_teams_link, list_of_pokemon_tuple)
        
        self.label_message.configure(text = 'Salvataggio completato, dati torneo disponibili!')
        self.after(3000, lambda : self.label_message.grid_forget())
        self.progressbar.grid_forget()
        self.confirm_choices_button.configure(state='normal')

    # funzione che viene chiamata quando si preme il tasto 'Conferma'
    def confirm_button_event(self):
        # si usa un thread per evitare che l'intera applicazione si blocchi per aspettare che la 
        # funzione chiamata finisca
        threading.Thread(target=self.start_downloading_and_saving).start()