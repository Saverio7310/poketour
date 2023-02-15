'''
Classe che serve a connettersi con il db locale. Tutte le operazioni avvengono qui dentro. Per
usare il db si deve creare un oggetto di questa classe.
'''

import sqlite3

class DBConnection():

    def start_connection(self):
        connection = sqlite3.connect('Database/tournament.db')
        return connection
    
    def exec_tables_creation(self, conn, cursor):
        result = conn.execute("""
        CREATE TABLE prova(
        link text,
        position integer
        )
        """)
        return result
    
    def create_table_new_tournament(self, conn, tour_code):
        statement1 = 'CREATE TABLE IF NOT EXISTS ?(link text PRIMARY KEY, standing integer)'.replace('?', tour_code)
        statement2 = """
        CREATE TABLE IF NOT EXISTS teams_?(
        link text,
        name text,
        ability text,
        tera text,
        item text,
        movea text,
        moveb text,
        movec text,
        moved text,
        typea text,
        typeb text,
        PRIMARY KEY(link, name)
        )
        """.replace('?', tour_code[:20])
        conn.execute(statement1)
        conn.execute(statement2)

    def insert_pokemons(self, conn, tour_code, list_of_tuples):
        statement = "INSERT INTO teams_! VALUES (?)".replace('!', tour_code)
        conn.executemany(statement, list_of_tuples)
        

