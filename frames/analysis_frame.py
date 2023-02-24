import customtkinter
from functools import partial
import Frames.tournament_window as tw
from Database.db_connection import DBConnection

# frame che serve a mostrare tutti i tornei salvati nel db e che apre la finesra relativa al torneo
# che si vuole analizzare
class AnalysisFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # si trovano tutti i tornei salvati nel db
        db = DBConnection()
        conn = db.start_connection()
        result = db.fetch_tournaments_data(conn)
        db.close_connection(conn)

        # per ogni torneo si crea un bottone che apre una finestra
        for i, tup in enumerate(result):
            btt = customtkinter.CTkButton(self, text= tup[0] + ', codice: ' + tup[1], command=partial(self.open_toplevel, tup[0], tup[1]))
            btt.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")

        self.toplevel_window = None

    # funzione che viene chiamata qunado si preme un bottone
    def open_toplevel(self, name, code):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = tw.TournamentWindow(self, tour_name=name, tour_code=code)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it