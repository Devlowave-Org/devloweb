import pymysql
from datetime import datetime


class DevloBDD:
    def __init__(self, user, password, host, port, database=None):
        self.database = database
        self.port = port
        self.host = host
        self.password = password
        self.user = user
        self.cursor = None
        self.connector = None

    def connection(self):
        self.connector = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port,
                                         database=self.database)  # Connection à la base de donnée.
        self.cursor = self.connector.cursor()  # Création du curseur.

    def reset_bdd(self):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("DROP TABLE IF EXISTS devloweb.users")
        self.cursor.execute("DROP TABLE IF EXISTS devloweb.magic_link")
        self.cursor.execute("DROP TABLE IF EXISTS devloweb.security")
        self.cursor.execute("DROP TABLE IF EXISTS devloweb.sites")
        self.create_bdd()
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def create_bdd(self):
        self.connection()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS devloweb.users (id INT PRIMARY KEY AUTO_INCREMENT, ja_id INT, name TEXT, password TEXT, email TEXT, email_verified BOOL DEFAULT FALSE, email_verification_code TEXT, email_verification_date TEXT, date_signin TEXT, date_last_login TEXT, active BOOL DEFAULT 1, admin BOOL DEFAULT 0);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS devloweb.security (id INT PRIMARY KEY AUTO_INCREMENT, ip TEXT, try INT DEFAULT 1,first TEXT, last TEXT, punition TEXT);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS devloweb.sites(id INT PRIMARY KEY AUTO_INCREMENT, ja_id TEXT, domain TEXT, theme TEXT, status INT DEFAULT 0);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS devloweb.magic_link(id INT PRIMARY KEY AUTO_INCREMENT, ja_id TEXT, code TEXT, date TEXT);")
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def inscire_ja(self, ja_id, name, password, email):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute(
            "INSERT INTO devloweb.users(ja_id, email, name, password, date_signin) VALUES (%s, %s, %s, %s, %s)",
            (ja_id, email, name, password, datetime.now()))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def delete_ja(self, email):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("DELETE FROM devloweb.users WHERE email = %s", (email,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def change_password(self, ja_id: str, password: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.users SET password = %s WHERE ja_id = %s", (password, ja_id))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def change_theme(self, ja_id: str, theme: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.sites SET theme = %s WHERE ja_id = %s", (theme, ja_id))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def change_domain(self, ja_id: str, url: str, domain: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.sites SET domain = %s WHERE ja_id = %s", (url, domain, ja_id))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def ja_exists(self, ja_id: str) -> bool:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT COUNT(*) FROM devloweb.users WHERE ja_id = %s", (ja_id,))
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def activer_email_ja(self, ja_id: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.users SET email_verified = 1 WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def desactiver_ja(self, ja_id: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.users SET email_verified = 0 WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def is_active(self, ja_id: int) -> bool:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT email_verified FROM devloweb.users WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def get_ja_by_mail(self, mail: str) -> list:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT ja_id, name, password, email, email_verified, email_verification_code, email_verification_date, date_signin, date_last_login, active, admin FROM devloweb.users WHERE email = %s", (mail,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        return self.cursor.fetchone()

    def get_ja_byid(self, ja_id: str) -> list:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT ja_id, name, password, email, email_verified, email_verification_code, email_verification_date, date_signin, date_last_login, active, admin FROM devloweb.users WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        return self.cursor.fetchone()

    def view_data_website(self, ja_id: str) -> list:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT ja_id, domain, theme, status FROM devloweb.sites WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        return self.cursor.fetchone()

    def get_site_by_ja(self, ja: str) -> list:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT ja_id, domain, theme, status FROM devloweb.sites WHERE ja_id = %s", (ja,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        return self.cursor.fetchone()

    """
    Partie Code de Vérification
    """

    def store_code(self, ja_id, code):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute(
            "UPDATE devloweb.users SET email_verification_code = %s, email_verification_date = %s WHERE ja_id = %s",
            (code, datetime.now(), ja_id))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def back_code_exists(self, code: str) -> bool:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT COUNT(*) FROM devloweb.users WHERE email_verification_code = %s", (code,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def get_code_via_jaid(self, ja_id: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT email_verification_code, ja_id, email_verification_date FROM devloweb.users WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        return self.cursor.fetchone()

    def update_code(self, ja_id: int, code: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.users SET email_verification_code = %s WHERE ja_id = %s", (code, ja_id))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def delete_code(self, ja_id: str) -> None:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.users SET email_verification_code = '' WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    """
    Partie sécurité :
    -> try
    """

    def init_try(self, ip):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("INSERT INTO devloweb.security(ip, first, last, punition) VALUES (%s, %s, %s, %s)",
                            (ip, datetime.now(), datetime.now(), datetime.now()))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def has_try(self, ip: str) -> bool:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT COUNT(*) FROM devloweb.security WHERE ip = %s", (ip,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def update_try(self, ip: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.security SET try = try + 1, last = %s WHERE ip = %s", (datetime.now(), ip))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

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
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT ip, try, first, last, punition FROM devloweb.security WHERE ip = %s", (ip,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        return self.cursor.fetchone()

    def reset_try(self, ip: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.security SET try = 1, first = last WHERE ip = %s", (ip,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def punish_try(self, ip: str, punition):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.security SET punition = %s WHERE ip = %s", (punition, ip))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def delete_try(self, ip: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("DELETE FROM devloweb.security WHERE ip = %s", (ip,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    """
    Partie site web
    """

    def init_website(self, ja_id, domain="", theme="basic"):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("INSERT INTO devloweb.sites(ja_id, domain, theme) VALUES (%s, %s, %s)",
                            (ja_id, domain, theme))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def enable_website(self, ja_id):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.sites SET status = 1 WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def get_ja_by_domain(self, domain):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT ja_id, domain, theme, status FROM devloweb.sites  WHERE domain=%s", (domain,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        try:
            return self.cursor.fetchall()[0]
        except IndexError:
            return None

    def set_domain_name(self, ja_id, domain):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("UPDATE devloweb.sites SET domain = %s WHERE ja_id = %s", (domain, ja_id))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    """
    partie magic link
    """

    def magic_link_exists(self, code: str) -> bool:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT COUNT(*) FROM devloweb.magic_link WHERE code = %s", (code,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        if self.cursor.fetchone()[0]:
            return True
        else:
            return False

    def get_magic_link_by_ja(self, ja_id: str) -> bool:
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT ja_id, code, date FROM devloweb.magic_link WHERE code = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        return self.cursor.fetchone()

    def store_magic_link(self, code, ja_id):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("INSERT INTO devloweb.magic_link(code, ja_id, date) VALUES (%s, %s, %s)",
                            (code, ja_id, datetime.now()))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def get_magic_link(self, code: str):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("SELECT ja_id, code, date FROM devloweb.magic_link WHERE code = %s", (code,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.
        return self.cursor.fetchone()

    def delete_magic_link(self, ja_id):
        self.connection()  # Connection avec la base de données.
        self.cursor.execute("DELETE FROM devloweb.magic_link WHERE ja_id = %s", (ja_id,))
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.