'''
Classe che serve a connettersi con il db locale. Tutte le operazioni avvengono qui dentro. Per
usare il db si deve creare un oggetto di questa classe.
'''

import sqlite3

'''
query per capire se esiste una tabella con un nome specifico
SELECT EXISTS (
    SELECT 
        name
    FROM 
        sqlite_schema 
    WHERE 
        type='table' AND 
        name='<table_name>'
    )
'''

class DBConnection():

    def start_connection(self):
        connection = sqlite3.connect('Database/tournament.db')
        return connection
    
    def create_table_new_tournament(self, conn, tour_code):
        statement1 = """
        CREATE TABLE IF NOT EXISTS tournaments(
        name text NOT NULL, 
        link text PRIMARY KEY
        )
        """
        statement2 = """
        CREATE TABLE IF NOT EXISTS ?(
        link text PRIMARY KEY, 
        standing integer
        )
        """.replace('?', tour_code)
        statement3 = """
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
        PRIMARY KEY(link, name),
        FOREIGN KEY(link) REFERENCES ? ON DELETE CASCADE ON UPDATE CASCADE
        )
        """.replace('?', tour_code)
        conn.execute(statement1)
        conn.execute(statement2)
        conn.execute(statement3)
        conn.commit()

    def insert_tournament(self, conn, tour_name, tour_code):
        statement = "INSERT OR IGNORE INTO tournaments VALUES (?, ?)"
        result = conn.execute(statement, (tour_name, tour_code)).fetchall()
        conn.commit()
        return result

    def insert_links(self, conn, tour_code, list_of_tuples):
        statement = "INSERT OR IGNORE INTO ! (link, standing) VALUES (?, ?)".replace('!', tour_code)
        conn.executemany(statement, list_of_tuples)
        conn.commit()

    def insert_pokemons(self, conn, tour_code, list_of_tuples):
        '''
        INSERT OR IGNORE INTO teams_h7kIYruNMePQMy4UZkMj 
        (link, name, ability, tera, item, movea, moveb, movec, moved) 
        VALUES ('azVMOBBztqFsyv6Oe03m', 'gholdengo', 'intimidate', 'steel', 'choice specs', 'protect', 'protect', 'protect', 'protect')
        '''
        statement = "INSERT OR IGNORE INTO teams_! (link, name, ability, tera, item, movea, moveb, movec, moved) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".replace('!', tour_code)
        conn.executemany(statement, list_of_tuples)
        conn.commit()

    def close_connection(self, conn):
        conn.close()
        

