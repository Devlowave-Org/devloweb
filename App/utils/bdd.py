import sqlite3
import time
from datetime import datetime

class DevloBDD:
    def __init__(self, name: str = "devlobdd"):
        self.conn = sqlite3.connect(name+".db")
        self.cursor = self.conn.cursor()
        # Creation de la base de donnée utilisateur
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(ja_id TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, date INT NOT NULL, active INT DEFAULT 0)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS verification(ja_id TEXT NOT NULL, code TEXT NOT NULL, date TEXT NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS security(ip TEXT NOT NULL,try INT DEFAULT 1, first TEXT NOT NULL, last TEXT NOT NULL, punition TEXT NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sites(ja_id TEXT NOT NULL, domain TEXT, url TEXT, theme TEXT NOT NULL, creation TEXT DEFAULT CURRENT_TIMESTAMP, titre TEXT, soustitre TEXT, description TEXT, logo TEXT NOT NULL, projet1 TEXT, projet11 TEXT, projet2 TEXT, projet22 TEXT, projet3 TEXT, projet33 TEXT, valeurs TEXT, valeur1 TEXT, valeur11 TEXT, valeur2 TEXT, valeur22 TEXT, valeur3 TEXT, valeur33 TEXT, valeur4 TEXT, valeur44 TEXT, text1 TEXT, text2 TEXT, titre1 TEXT, titre2 TEXT)""")
        self.conn.commit()

    def reset_bdd(self):
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.cursor.execute("DROP TABLE IF EXISTS verification")
        self.cursor.execute("DROP TABLE IF EXISTS security")
        self.cursor.execute("DROP TABLE IF EXISTS sites")
        self.conn.commit()

    def boom_boom(self, form_data, ja_id):
        for key, value in form_data.items():
            sqlformated = "UPDATE sites SET {} = (?) WHERE ja_id = (?)".format(key)
            self.cursor.execute(sqlformated, (value[0], ja_id))
            self.conn.commit()

    def inscire_ja(self, ja_id, email, password):
        self.cursor.execute("INSERT INTO users(ja_id, email, password, date) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", (ja_id, email, password))
        self.conn.commit()

    def delete_ja(self, email):
        self.cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        self.conn.commit()

    def create_website(self, ja_id):
        print("Création du site de l'utilisateur : " + ja_id)
        self.cursor.execute("INSERT INTO sites(ja_id, url, theme, creation, titre, description, logo) VALUES (?, 'example.com', 'thyo', CURRENT_TIMESTAMP, 'Un titre', 'Une description', 'logo.png')", (ja_id,))
        self.conn.commit()
        print("Site créé !")
        
    def change_theme(self, ja_id: str, theme : str):
        self.cursor.execute("UPDATE sites SET theme = ? WHERE ja_id = ?", (theme, ja_id))
        self.conn.commit()

    def change_domain(self, ja_id: str, url: str, domain : str):
        self.cursor.execute("UPDATE sites SET url = ?, domain = ? WHERE ja_id = ?", (url, domain, ja_id))
        self.conn.commit()
        
    def ja_exists(self, ja_id: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE ja_id = ?", (ja_id,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def activer_ja(self, ja_id: str):
        self.cursor.execute("UPDATE users SET active = 1 WHERE ja_id = ?", (ja_id,))
        self.conn.commit()

    def desactiver_ja(self, ja_id: str):
        self.cursor.execute("UPDATE users SET active = 0 WHERE ja_id = ?", (ja_id,))
        self.conn.commit()

    def is_active(self, ja_id: int) -> bool:
        self.cursor.execute("SELECT active FROM users WHERE ja_id = ?", (ja_id,))
        try:
            if self.cursor.fetchone()[0]:
                return True
            else:
                return False
        except IndexError as e:
            return False

    def get_ja_by_mail(self, mail: str) -> list:
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (mail,))
        return self.cursor.fetchone()

    def get_ja_byid(self, ja_id: str) -> list:
        self.cursor.execute("SELECT * FROM users WHERE ja_id = ?", (ja_id,))
        return self.cursor.fetchone()
    
    def view_data_website(self, ja_id: str) -> list:
        self.cursor.execute("SELECT * FROM sites WHERE ja_id = ?", (ja_id,))
        return self.cursor.fetchone()
    
    def get_site_by_ja(self, ja: str) -> list:
        self.cursor.execute("SELECT * FROM sites WHERE ja_id = ?", (ja,))
        return self.cursor.fetchone()

    """
    Partie Code de Vérification
    """
    def store_code(self, ja_id, code):
        self.cursor.execute("INSERT INTO verification(ja_id, code, date) VALUES (?, ?, ?)", (ja_id, code, datetime.now()))
        self.conn.commit()

    def code_exists(self, code: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM verification WHERE code = ?", (code,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def get_code_via_jaid(self, ja_id: str):
        self.cursor.execute("SELECT ja_id, code, datetime(date, 'localtime') FROM verification WHERE ja_id = ?", (ja_id,))
        return self.cursor.fetchone()

    def update_code(self, ja_id: int, code: str):
        self.cursor.execute("UPDATE verification SET code = ? WHERE ja_id = ?", (code, ja_id))
        self.conn.commit()

    def delete_code(self, code: str) -> None:
        self.cursor.execute("DELETE FROM verification WHERE code = ?", (code,))
        self.conn.commit()


    """
    Partie sécurité :
    -> try
    """
    def init_try(self, ip):
        self.cursor.execute("INSERT INTO security(ip, first, last, punition) VALUES (?, ?, ?, ?)", (ip, datetime.now(), datetime.now(), datetime.now()))
        self.conn.commit()

    def has_try(self, ip: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM security WHERE ip = ?", (ip,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def update_try(self, ip: str):
        self.cursor.execute("UPDATE security SET try = try + 1, last = ? WHERE ip = ?", (datetime.now(), ip,))
        self.conn.commit()

    def add_try(self, ip: str):
        if self.has_try(ip):
            self.update_try(ip)
        else:
            self.init_try(ip)

    def get_try(self, ip: str):
        """
        Les dates sont retournées en format local.
        :param ip:
        :return:
        """
        self.cursor.execute("SELECT ip, try, first, last, punition FROM security WHERE ip = ?", (ip,))
        return self.cursor.fetchone()

    def reset_try(self, ip: str):
        self.cursor.execute("UPDATE security SET try = 1, first = last WHERE ip = ?", (ip,))
        self.conn.commit()

    def punish_try(self, ip: str, punition):
        self.cursor.execute("UPDATE security SET punition = ? WHERE ip = ?", (punition, ip))
        self.conn.commit()

    def delete_try(self, ip: str):
        self.cursor.execute("DELETE FROM security WHERE ip = ?", (ip,))
        self.conn.commit()

    def quit_bdd(self):
        self.conn.close()


    """
    Partie Blog
    Oui j'ai pas de vie
    """
    
    def post_data(self, slug: str) -> list:
        self.cursor.execute("SELECT * FROM blog WHERE slug = ? AND website = 'PROD'", (slug,))
        return self.cursor.fetchone()
    
    def post_exists(self, slug: str) -> bool:
        self.cursor.execute("SELECT * FROM sites WHERE slug = ?", (slug,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False


if __name__ == '__main__':
    bdd = DevloBDD()
    print(bdd.is_active(8166))