import customtkinter
from functools import partial
import Frames.tournament_window as tw
from Database.db_connection import DBConnection

class AnalysisFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        db = DBConnection()
        conn = db.start_connection()
        result = db.fetch_tournaments_data(conn)
        db.close_connection(conn)

        for i, tup in enumerate(result):
            btt = customtkinter.CTkButton(self, text= tup[0] + ', codice: ' + tup[1], command=partial(self.open_toplevel, tup[0], tup[1]))
            btt.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")

        self.toplevel_window = None

    def open_toplevel(self, name, code):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = tw.TournamentWindow(self, tour_name=name, tour_code=code)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it