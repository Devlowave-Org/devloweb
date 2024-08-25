import sqlite3
import time
from datetime import datetime

class DevloBDD:
    def __init__(self, name: str = "devlobdd"):
        self.conn = sqlite3.connect(name+".db")
        self.cursor = self.conn.cursor()
        # Creation de la base de donnée utilisateur
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(ja_id TEXT NOT NULL, email TEXT NOT NULL, name TEXT NOT NULL ,password TEXT NOT NULL, date INT NOT NULL, active INT DEFAULT 0)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS verification(ja_id TEXT NOT NULL, code TEXT NOT NULL, date TEXT NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS security(ip TEXT NOT NULL,try INT DEFAULT 1, first TEXT NOT NULL, last TEXT NOT NULL, punition TEXT NOT NULL)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS sites(ja_id TEXT NOT NULL, domain TEXT, theme TEXT NOT NULL, active INT DEFAULT 0)""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS magic_link(code TEXT NOT NULL, ja_id TEXT NOT NULL, date TEXT NOT NULL)""")

        self.conn.commit()
        print(f"{name} est prêt")

    def reset_bdd(self):
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.cursor.execute("DROP TABLE IF EXISTS verification")
        self.cursor.execute("DROP TABLE IF EXISTS security")
        self.cursor.execute("DROP TABLE IF EXISTS sites")
        self.conn.commit()


    def inscire_ja(self, ja_id, email, password, name):
        self.cursor.execute("INSERT INTO users(ja_id, email, name, password, date) VALUES (?, ?, ?, ?, ?)", (ja_id, email, name, password, datetime.now()))
        self.conn.commit()

    def delete_ja(self, email):
        self.cursor.execute("DELETE FROM users WHERE email = ?", (email,))
        self.conn.commit()

    def change_password(self, ja_id: str, password: str):
        self.cursor.execute("UPDATE users SET password = ? WHERE ja_id = ?", (password, ja_id))
        self.conn.commit()


        
    """ def change_theme(self, ja_id: str, theme : str):
        self.cursor.execute("UPDATE sites SET theme = ? WHERE ja_id = ?", (theme, ja_id))
        self.conn.commit()

    def change_domain(self, ja_id: str, url: str, domain : str):
        self.cursor.execute("UPDATE sites SET url = ?, domain = ? WHERE ja_id = ?", (url, domain, ja_id))
        self.conn.commit()
        """
        
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
        if self.cursor.fetchone()[0]:
            return True
        else:
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

    def get_all_ja_with_website(self):
        self.cursor.execute("SELECT ja_id FROM sites")
        return self.cursor.fetchall()

    def get_website_status_based_on_ja_id(self, ja_id):
        self.cursor.execute("SELECT active FROM sites WHERE ja_id = ?", (ja_id,))
        self.cursor.fetchone()
    
    
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
        self.cursor.execute("SELECT ja_id, code, date FROM verification WHERE ja_id = ?", (ja_id,))
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


    """
    Partie site web
    """
    def init_website(self, ja_id, domain="", theme="basic"):
        self.cursor.execute("INSERT INTO sites(ja_id, domain, theme) VALUES (?, ?, ?)", (ja_id, domain, theme))
        self.conn.commit()

    def enable_website(self, ja_id):
        self.cursor.execute("UPDATE sites SET active = 1 WHERE ja_id = ?", (ja_id,))
        self.conn.commit()

    def get_ja_by_domain(self, domain):
        self.cursor.execute("SELECT * FROM sites  WHERE domain=?", (domain,))
        try:
            return self.cursor.fetchall()[0]
        except IndexError:
            return None

    def set_domain_name(self, ja_id, domain):
        self.cursor.execute("UPDATE sites SET domain = ? WHERE ja_id = ?", (domain, ja_id))
        self.conn.commit()


    """
    partie magic link
    """
    def magic_link_exists(self, code: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM magic_link WHERE code = ?", (code,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def get_magic_link_by_ja(self, ja_id: str) -> bool:
        self.cursor.execute("SELECT * FROM magic_link WHERE code = ?", (ja_id,))
        return self.cursor.fetchone()

    def store_magic_link(self, code, ja_id):
        self.cursor.execute("INSERT INTO magic_link(code, ja_id, date) VALUES (?, ?, ?)", (code, ja_id, datetime.now()))
        self.conn.commit()

    def get_magic_link(self, code: str):
        self.cursor.execute("SELECT * FROM magic_link WHERE code = ?", (code,))
        return self.cursor.fetchone()

    def delete_magic_link(self, ja_id):
        self.cursor.execute("DELETE FROM magic_link WHERE ja_id = ?", (ja_id,))
        self.conn.commit()

    def quit_bdd(self):
        self.conn.close()


    """
    Partie Blog
    Oui j'ai pas de vie
    """
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
    """

if __name__ == '__main__':
    bdd = DevloBDD()
    print(bdd.is_active(8166))