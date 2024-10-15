import pymysql
from datetime import datetime

class DevloBDD:
    def __init__(self, user, password, host, port, database=None):
        if database is None:
            self.database = "devloweb"
        else:
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
        self.cursor = self.connector.cursor()

    def get_connection(self):
        return pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port,
                               database=self.database)

    def close(self):
        self.cursor.close()
        self.connector.close()


    def reset_bdd(self):
        self.execute_query("DROP TABLE IF EXISTS users;")
        self.execute_query("DROP TABLE IF EXISTS magic_link;")
        self.execute_query("DROP TABLE IF EXISTS security;")
        self.execute_query("DROP TABLE IF EXISTS sites;")
        self.create_bdd()


    def create_bdd(self):
        self.connection()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY AUTO_INCREMENT, ja_id INT, name TEXT, password TEXT, email TEXT, email_verified BOOL DEFAULT FALSE, email_verification_code TEXT, email_verification_date TEXT, date_signin TEXT, date_last_login TEXT, active BOOL DEFAULT 1, admin BOOL DEFAULT 0);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS security (id INT PRIMARY KEY AUTO_INCREMENT, ip TEXT, try INT DEFAULT 1,first TEXT, last TEXT, punition TEXT);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sites(id INT PRIMARY KEY AUTO_INCREMENT, ja_id TEXT, domain TEXT, theme TEXT, status INT DEFAULT 0);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS magic_link(id INT PRIMARY KEY AUTO_INCREMENT, ja_id TEXT, code TEXT, date TEXT);")
        self.cursor.close()  # Fermeture du curseur.
        self.connector.commit()  # Enregistrement dans la base de donnée.
        self.connector.close()  # Fermeture de la connexion.

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        """
        Méthode utilitaire pour exécuter des requêtes SQL avec gestion automatique de la connexion.
        """
        result = None
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    if fetchone:
                        result = cursor.fetchone()
                    elif fetchall:
                        result = cursor.fetchall()
                    connection.commit()
        except pymysql.MySQLError as e:
            print(f"Erreur SQL: {e}")
        return result

    def inscire_ja(self, ja_id, name, password, email):
        query = """
        INSERT INTO users(ja_id, email, name, password, date_signin) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.execute_query(query, (ja_id, email, name, password, datetime.now()))

    def delete_ja(self, email):
        query = """DELETE FROM users WHERE email = %s"""
        self.execute_query(query, (email,))

    def change_password(self, ja_id: str, password: str):
        self.connection()  # Connection avec la base de données.
        query = """UPDATE users SET password = %s WHERE ja_id = %s"""
        self.execute_query(query, (password, ja_id))

    def change_theme(self, ja_id: str, theme: str):
        self.execute_query("UPDATE sites SET theme = %s WHERE ja_id = %s", (theme, ja_id))


    def change_domain(self, ja_id: str, url: str, domain: str):
        self.execute_query("UPDATE sites SET domain = %s WHERE ja_id = %s", (url, domain, ja_id))


    def ja_exists(self, ja_id: str) -> bool:
        result = self.execute_query("SELECT COUNT(*) FROM users WHERE ja_id = %s", (ja_id,), fetchone=True)
        return result[0] > 0


    def activer_email_ja(self, ja_id: str):
        self.execute_query("UPDATE users SET email_verified = 1 WHERE ja_id = %s", (ja_id,))


    def desactiver_ja(self, ja_id: str):
        self.execute_query("UPDATE users SET email_verified = 0 WHERE ja_id = %s", (ja_id,))


    def is_active(self, ja_id: int) -> bool:
        result = self.execute_query("SELECT email_verified FROM users WHERE ja_id = %s", (ja_id,), fetchone=True)
        return result[0] == 1

    def get_ja_by_mail(self, mail: str) -> list:
        result = self.execute_query("SELECT ja_id, name, password, email, email_verified, email_verification_code, email_verification_date, date_signin, date_last_login, active, admin FROM users WHERE email = %s", (mail,), fetchone=True)
        return result

    def get_ja_byid(self, ja_id: str) -> list:
        result = self.execute_query("SELECT ja_id, name, password, email, email_verified, email_verification_code, email_verification_date, date_signin, date_last_login, active, admin FROM users WHERE ja_id = %s", (ja_id,), fetchone=True)
        return result

    def view_data_website(self, ja_id: str) -> tuple:
        result = self.execute_query("SELECT ja_id, domain, theme, status FROM sites WHERE ja_id = %s", (ja_id,), fetchone=True)
        return result

    def get_site_by_ja(self, ja: str) -> list:
        result = self.execute_query("SELECT ja_id, domain, theme, status FROM sites WHERE ja_id = %s", (ja,), fetchone=True)
        print(f"Result : {result}")
        return result

    """USED BY ADMIN PANNEL"""

    def fetch_all_ja_ids_with_website(self):
        result = self.execute_query("SELECT ja_id FROM sites", fetchall=True)
        return result

    def get_website_status_by_id(self, ja_id):
        result = self.execute_query("SELECT status FROM sites WHERE ja_id = %s", (ja_id,), fetchone=True)
        return result

    def update_website_status_by_id(self, ja_id, status):
        self.execute_query("UPDATE sites SET status = %s WHERE ja_id = %s", (status, ja_id))

    def get_ja_name_by_id(self, ja_id):
        result = self.execute_query("SELECT name FROM users WHERE ja_id = %s", (ja_id,), fetchone=True)
        return result

    def get_ja_id_by_name(self, name):
        result = self.execute_query("SELECT ja_id FROM users WHERE name = %s", (name,), fetchone=True)
        return result

    def get_ja_domain_by_id(self, ja_id):
        result = self.execute_query("SELECT domain FROM sites WHERE ja_id = %s", (ja_id,), fetchone=True)
        return result

    def get_ja_id_by_domain(self, domain):
        result = self.execute_query("SELECT ja_id FROM sites WHERE domain = %s", (domain,), fetchone=True)
        return result

    """
    Partie Code de Vérification
    """

    def store_code(self, ja_id, code):
        self.execute_query(
            "UPDATE users SET email_verification_code = %s, email_verification_date = %s WHERE ja_id = %s",
            (code, datetime.now(), ja_id))

    def back_code_exists(self, code: str) -> bool:
        result = self.execute_query("SELECT COUNT(*) FROM users WHERE email_verification_code = %s", (code,), fetchone=True)
        return result[0] > 0

    def get_code_via_jaid(self, ja_id: str):
        result = self.execute_query("SELECT email_verification_code, ja_id, email_verification_date FROM users WHERE ja_id = %s", (ja_id,), fetchone=True)
        return result

    def update_code(self, ja_id: int, code: str):
        self.execute_query("UPDATE users SET email_verification_code = %s WHERE ja_id = %s", (code, ja_id))


    def delete_code(self, ja_id: str) -> None:
        self.execute_query("UPDATE users SET email_verification_code = '' WHERE ja_id = %s", (ja_id,))

    """
    Partie sécurité :
    -> try
    """

    def init_try(self, ip):
        self.execute_query("INSERT INTO security(ip, first, last, punition) VALUES (%s, %s, %s, %s)",
                            (ip, datetime.now(), datetime.now(), datetime.now()))


    def has_try(self, ip: str) -> bool:
        result = self.execute_query("SELECT COUNT(*) FROM security WHERE ip = %s", (ip,), fetchone=True)
        return result[0] > 0


    def update_try(self, ip: str):
        self.execute_query("UPDATE security SET try = try + 1, last = %s WHERE ip = %s", (datetime.now(), ip))


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
        result = self.execute_query("SELECT ip, try, first, last, punition FROM security WHERE ip = %s", (ip,), fetchone=True)
        return result

    def reset_try(self, ip: str):
        self.execute_query("UPDATE security SET try = 1, first = last WHERE ip = %s", (ip,))


    def punish_try(self, ip: str, punition):
        self.execute_query("UPDATE security SET punition = %s WHERE ip = %s", (punition, ip))


    def delete_try(self, ip: str):
        self.execute_query("DELETE FROM security WHERE ip = %s", (ip,))

    """
    Partie site web
    """

    def init_website(self, ja_id, domain="", theme="basic"):
        self.execute_query("INSERT INTO sites(ja_id, domain, theme) VALUES (%s, %s, %s)",
                            (ja_id, domain, theme))

    def enable_website(self, ja_id):
        self.execute_query("UPDATE sites SET status = 1 WHERE ja_id = %s", (ja_id,))

    def get_ja_by_domain(self, domain):
        result = self.execute_query("SELECT ja_id, domain, theme, status FROM sites  WHERE domain=%s", (domain,), fetchone=True)
        return result

    def ask_hebergement(self, ja_id):
        self.execute_query("UPDATE sites SET status = 2 WHERE ja_id = %s", (ja_id,))


    def set_domain_name(self, ja_id, domain):
        self.execute_query("UPDATE sites SET domain = %s WHERE ja_id = %s", (domain, ja_id))

    """
    partie magic link
    """

    def magic_link_exists(self, code: str) -> bool:
        result = self.execute_query("SELECT COUNT(*) FROM magic_link WHERE code = %s", (code,), fetchone=True)
        return result[0] > 0


    def get_magic_link_by_ja(self, ja_id: str) -> bool:
        result = self.execute_query("SELECT ja_id, code, date FROM magic_link WHERE code = %s", (ja_id,), fetchone=True)
        return result


    def store_magic_link(self, code, ja_id):
        self.execute_query("INSERT INTO magic_link(code, ja_id, date) VALUES (%s, %s, %s)",
                            (code, ja_id, datetime.now()))


    def get_magic_link(self, code: str):
        result = self.execute_query("SELECT ja_id, code, date FROM magic_link WHERE code = %s", (code,), fetchone=True)
        return result

    def delete_magic_link(self, ja_id):
        self.execute_query("DELETE FROM magic_link WHERE ja_id = %s", (ja_id,))
