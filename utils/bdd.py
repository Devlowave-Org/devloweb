import sqlite3
import time


class DevloBDD:
    def __init__(self):
        self.conn = sqlite3.connect('devloweb.db')
        self.cursor = self.conn.cursor()
        # Creation de la base de donnée utilisateur
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(ja_id INT NOT NULL, email TEXT NOT NULL, password 
        TEXT NOT NULL, date INT NOT NULL, active INT DEFAULT 0)""")
        self.conn.commit()



    def inscire_ja(self, ja_id, email, password):
        date = time.time()
        self.cursor.execute("INSERT INTO users(ja_id, email, password, date) VALUES (?, ?, ?, ?)", (ja_id, email, password, date))
        self.conn.commit()

    def ja_exists(self, ja_id: int) -> list:
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE ja_id = ?", (ja_id,))
        return self.cursor.fetchone()




if __name__ == '__main__':
    bdd = DevloBDD()
    bdd.inscire_ja(8166, '<EMAIL>', '<PASSWORD>')