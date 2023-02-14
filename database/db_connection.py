'''
Classe che serve a connettersi con il db locale. Tutte le operazioni avvengono qui dentro. Per
usare il db si deve creare un oggetto di questa classe.
'''

import sqlite3

class DBConnection():

    def start_connection(self):
        connection = sqlite3.connect('Database/tournament.db')
        return connection.cursor()
    
    def exec_tables_creation(self, cursor):
        result = cursor.execute("""
        CREATE TABLE prova(
        link text,
        position integer
        )
        """)
        return result

