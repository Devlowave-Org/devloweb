import sqlite3
import time


class DevloBDD:
    def __init__(self):
        self.conn = sqlite3.connect('devloweb.db')
        self.cursor = self.conn.cursor()
        # Creation de la base de donnée utilisateur
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(ja_id TEXT NOT NULL, email TEXT NOT NULL, password 
        TEXT NOT NULL, date INT NOT NULL, active INT DEFAULT 0)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS verification(ja_id TEXT NOT NULL, code TEXT NOT NULL, try 
                INT NOT NULL, date INT NOT NULL)""")
        self.conn.commit()



    def inscire_ja(self, ja_id, email, password):
        date = time.time()
        self.cursor.execute("INSERT INTO users(ja_id, email, password, date) VALUES (?, ?, ?, ?)", (ja_id, email, password, date))
        self.conn.commit()

    def ja_exists(self, ja_id: int) -> list:
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE ja_id = ?", (ja_id,))
        return self.cursor.fetchone()

    def activer_ja(self, ja_id: int):
        self.cursor.execute("UPDATE users SET active = 1 WHERE ja_id = ?", (ja_id,))
        self.conn.commit()

    def is_active(self, ja_id: int) -> bool:
        self.cursor.execute("SELECT active FROM users WHERE ja_id = ?", (ja_id,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False


if __name__ == '__main__':
    bdd = DevloBDD()
    print(bdd.is_active(8166))