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

    # creazione collegamento con il db
    def start_connection(self):
        connection = sqlite3.connect('Database/tournament.db')
        return connection
    
    # creazione tabelle (se non esistono già)
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

    # inserimento di un nuovo torneo nella tabella dei tornei
    def insert_tournament(self, conn, tour_name, tour_code):
        statement = "INSERT OR IGNORE INTO tournaments VALUES (?, ?)"
        result = conn.execute(statement, (tour_name, tour_code)).fetchall()
        conn.commit()
        return result

    # inserimento dei link dei team nella tabella del torneo associato
    def insert_links(self, conn, tour_code, list_of_tuples):
        statement = "INSERT OR IGNORE INTO ! (link, standing) VALUES (?, ?)".replace('!', tour_code)
        conn.executemany(statement, list_of_tuples)
        conn.commit()

    # inserimento di un pokemon nella tabella relativa la torneo
    def insert_pokemons(self, conn, tour_code, list_of_tuples):
        '''
        INSERT OR IGNORE INTO teams_h7kIYruNMePQMy4UZkMj 
        (link, name, ability, tera, item, movea, moveb, movec, moved) 
        VALUES ('azVMOBBztqFsyv6Oe03m', 'gholdengo', 'intimidate', 'steel', 'choice specs', 'protect', 'protect', 'protect', 'protect')
        '''
        statement = "INSERT OR IGNORE INTO teams_! (link, name, ability, tera, item, movea, moveb, movec, moved) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".replace('!', tour_code)
        conn.executemany(statement, list_of_tuples)
        conn.commit()

    # query che va a controllare che il torneo che si vorrebbe salvare non sia già stato inserito
    def check_already_saved_tournament(self, conn, tour_code):
        statement = "SELECT count(*) FROM tournaments WHERE link = ?"
        cursor = conn.cursor()
        cursor.execute(statement, (tour_code, ))
        return cursor.fetchone()
    
    # query che ritorna tutti i dati inseriti nella tabella 'tournaments'
    def fetch_tournaments_data(self, conn):
        statement = 'SELECT name, link FROM tournaments'
        cursor = conn.cursor()
        cursor.execute(statement)
        return cursor.fetchall()
    
    # 3 query che ritornano le informazioni generali relative ad un torneo: numero di partecipanti,
    # classifica dei pokemon e classifica delle tera utilizzate
    def get_general_info(self, conn, tour_code):
        statement1 = 'SELECT count(link) FROM ?'.replace('?', tour_code)
        statement2 = 'SELECT name, count(name) FROM teams_? GROUP BY name ORDER BY count(name) DESC'.replace('?', tour_code)
        statement3 = 'SELECT tera, count(tera) FROM teams_? GROUP BY tera ORDER BY count(tera) DESC'.replace('?', tour_code)
        cursor = conn.cursor()
        cursor.execute(statement1)
        participants_number = cursor.fetchone()
        cursor.execute(statement2)
        top_poke = cursor.fetchall()
        cursor.execute(statement3)
        top_tera = cursor.fetchall()
        return (participants_number, top_poke, top_tera)
    
    # 4 query che ritornano le informazioni specifiche per ogni pokemon selezionato: tutti i moveset
    # (che vengono poi contati separatamente), classifica degli oggetti, delle abilità e delle tera
    def get_specific_poke_info(self, conn, tour_code, poke_name):
        statement1 = 'SELECT movea, moveb, movec, moved FROM teams_{code} WHERE name = \'{name}\''.format(code=tour_code, name=poke_name)
        statement2 = 'SELECT item, count(item) FROM teams_{code} WHERE name = \'{name}\' GROUP BY item ORDER BY count(item) DESC'.format(code=tour_code, name=poke_name)
        statement3 = 'SELECT ability, count(ability) FROM teams_{code} WHERE name = \'{name}\' GROUP BY ability ORDER BY count(ability) DESC'.format(code=tour_code, name=poke_name)
        statement4 = 'SELECT tera, count(tera) FROM teams_{code} WHERE name = \'{name}\' GROUP BY tera ORDER BY count(tera) DESC'.format(code=tour_code, name=poke_name)
        cursor = conn.cursor()
        cursor.execute(statement1)
        top_moveset = cursor.fetchall()
        cursor.execute(statement2)
        top_item = cursor.fetchall()
        cursor.execute(statement3)
        top_ability = cursor.fetchall()
        cursor.execute(statement4)
        top_tera = cursor.fetchall()
        return (top_moveset, top_tera, top_ability, top_item)

    # chiusura delle connessiona al db
    def close_connection(self, conn):
        conn.close()