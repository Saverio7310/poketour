import customtkinter
import threading
import tkinter
from tkinter import ttk
from Database.db_connection import DBConnection

class TournamentWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, tour_name='Nome Torneo', tour_code='Codice Torneo',  **kwargs):
        super().__init__(*args, **kwargs)

        #parametri generali finestra
        self.geometry("800x600")
        self.title('Analisi ' + str(tour_name))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #recupero dati generali sul torneo aperto
        db = DBConnection()
        conn = db.start_connection()
        participants, top_poke, top_tera = db.get_general_info(conn, tour_code)

        # funzione che ritorna i moveset più usati. Per come è strutturato il db era l'unica classifica
        # che non poteva essere generata direttamente con SQLite. Trasformo le tuple dei moveset in
        # insiemi affinché due moveset uguali ma con ordini differenti delle mosse risultino uguali.
        # Poi faccio partire due cicli uguali: confronto ogni moveset con tutti gli altri e per ogni
        # moveset uguale aumento la variabile di 1, sostituisco l'insieme con una variabile nota (-1)
        # e rimuovo l'occorrenza in modo tale da non ricontare gli stessi elementi. Infine inserisco
        # in una lista il moveset con il numero di occorrenze e lo ordino in modo decrescente.
        dict_poke_info = dict()
        def get_movesets(top_moveset):
            moveset_list = list()
            for moveset in top_moveset:
                moveset_list.append(set(moveset))
            moveset_list_final = list()
            for move_set1 in moveset_list:
                num = 0
                for ind, move_set2 in enumerate(moveset_list):
                    if move_set2 == move_set1 and move_set2 != -1:
                        num += 1
                        moveset_list.insert(ind, -1)
                        moveset_list.remove(move_set2)
                if move_set1 != -1:
                    moveset_list_final.append((move_set1, num))
            moveset_list_final.sort(key=lambda a : a[1], reverse=True)
            return moveset_list_final

       # funzione che parte in un thread diverso dal principale in modo tale da avere i dati 
       # subito disponibili. Mi collego al db e per ogni pokemon presente nella tabella prendo
       # informazioni specifiche
        def get_data():
            db = DBConnection()
            conn = db.start_connection()
            for poke, _ in top_poke:
                moveset, tera, ability, item = db.get_specific_poke_info(conn, tour_code, poke)
                movesets = get_movesets(moveset)
                dict_poke_info[poke] = (movesets, tera, ability, item)

        # thread che fa partire la funzione in modo tale da scaricare i dati in un altro thread ed 
        # averli subito disponibili
        threading.Thread(target=get_data).start()

        # Frame centrale della finestra
        self.frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.frame.grid(row=0, column=0, columnspan = 2, sticky='nsew', padx=10, pady=10)
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid_rowconfigure((0, 2), weight=1)

        # Label con il nome del torneo
        self.label_name = customtkinter.CTkLabel(self.frame, text=tour_name)
        self.label_name.cget("font").configure(size=50)
        self.label_name.grid(row=0, column=0, columnspan=2, sticky='nsew')

        # Label con il nomero dei partecipanti
        str_to_show = 'Dati generati su un totale di ? partecipanti'.replace('?', str(participants[0]))
        self.label_part = customtkinter.CTkLabel(self.frame, text=str_to_show, anchor='sw')
        #self.label_part.cget("font").configure(size=50)
        self.label_part.grid(row=1, column=0, columnspan=2, sticky='nsew')


        # Stile associato alle due tabelle 
        style = ttk.Style()
        # Tema di default
        style.theme_use("default")

        '''
        # Configure our treeview colors
        style.configure("Treeview", 
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
            )
        # Change selected color
        style.map('Treeview', background=[('selected', 'blue')])
        '''


        # Configurazione dello stile sia per le righe delle tabelle che per gli header delle colonne
        style.configure(
            "Treeview",
            background="#333333",
            foreground="#DCE4EE",
            fieldbackground="#333333",
            rowheight=30,
            )
        style.configure(
            "Treeview.Heading",
            background="#333333",
            foreground="#DCE4EE",
            #relief="flat",
            rowheight=30,
            font=(None, 20)
            )
        # Colore delle righe quando selezionate
        style.map('Treeview', background=[('selected', '#3B8ED0')])
        style.map('Treeview.Heading', background=[('selected', '#3B8ED0')])

        # Tabella con la classifica dei poke più usati
        self.top_poke_tree = ttk.Treeview(self.frame, show='headings')
        self.top_poke_tree.grid(row=2, column=0, sticky='nsew')
        self.top_poke_tree['columns'] = ('name', 'usage')
        self.top_poke_tree.column('name', minwidth=160)
        self.top_poke_tree.column('usage', width=50, minwidth=40)
        self.top_poke_tree.heading('name', text='Name', anchor=tkinter.W)
        self.top_poke_tree.heading('usage', text='Usage', anchor=tkinter.W)

        # Riempimento della tabella con i dati
        for tup in top_poke:
            self.top_poke_tree.insert('', tkinter.END, values=tup)

        # Frame che viene mostrato quando si clicca due volte una riga
        self.info_poke_frame = customtkinter.CTkFrame(self, corner_radius=10)
        #self.info_poke_frame.grid_columnconfigure((0, 1), weight=1)
        #self.info_poke_frame.grid_rowconfigure((0, 2), weight=1)
        
        # funzione che parte quando si clicca due volte una riga. Preso il nome del poke contenuto
        # nella riga selezionata, accedo al valore contenuto nel dizionario associato a quel nome.
        # il valore contenuto è una tupla formata da 4 liste. Fatto ciò, mostro il frame e butto
        # dentro le le informazioni raccolte
        def click(e):
            # Mette in evidenza la riga selezionate
            selected = self.top_poke_tree.focus()
            # Prende il valore contenuto nella riga selezionata
            values = self.top_poke_tree.item(selected, 'values')
            moveset, tera, ability, item = dict_poke_info[values[0]]
            self.info_poke_frame.grid(row=3, column=0, columnspan = 2, sticky='sew', padx=10, pady=10)
            #self.info_poke_frame.grid_propagate(0)
            #self.info_poke_frame.configure(width=300)
            
            print(*moveset, sep='\n')
            print(tera)
            print(ability)
            print(item)

        # Associo alla tabella della lista dei poke la funzione 'click' quando di clicca due volte
        self.top_poke_tree.bind('<Double-1>', click)

        # Tabella con la classifica delle tera più usate
        self.top_tera_tree = ttk.Treeview(self.frame, show='headings')
        self.top_tera_tree.grid(row=2, column=1, sticky='nsew')
        self.top_tera_tree['columns'] = ('tera', 'usage')
        self.top_tera_tree.column('tera', minwidth=160)
        self.top_tera_tree.column('usage', width=50, minwidth=40)
        self.top_tera_tree.heading('tera', text='Teratype', anchor=tkinter.W)
        self.top_tera_tree.heading('usage', text='Usage', anchor=tkinter.W)

        # Riempimento della tabella con i dati
        for tup in top_tera:
            self.top_tera_tree.insert('', tkinter.END, values=tup)