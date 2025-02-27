import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DevloMail:
    def __init__(self):
        self.host = os.environ["SMTP_HOST"]
        self.port = os.environ["SMTP_PORT"]
        self.sender = os.environ["SMTP_USER"]
        self.app_pass = os.environ['SMPT_PASSWORD']
        self.context = ssl.create_default_context()

    def verification_email(self, target, code):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Code de vérification"
        message["From"] = self.sender
        message["To"] = target

        text = """\
        Ceci est un message de Devloweb, voici ton code afin d'activer ton compte : {code}"""
        text = text.format(code=code)

        html = """\
        <html>
          <body>
            <p>Salut !<br>
                Ceci est un message de Devloweb,<br>
                Nous avons bien reçu ta demande d'inscription !<br>
                Afin d'activer ton compte voici le code : <span style="font-weight: bold;">{code}</span><br>
                <a href="https://{server_name}/verification?code={code}">Vérifier ici !</a>
            </p>
          </body>
        </html>
        """
        html = html.format(code=code, server_name=os.environ['SERVER_NAME'])
        self.send_mail(text, html, message, target)

    def magic_link_mail(self, target, code):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Réinitialisation du mot de passe"
        message["From"] = self.sender
        message["To"] = target

        text = """\
                Ceci est un message de Devloweb"""
        text = text.format(code=code)

        html = """\
                <html>
                  <body>
                    <p>Salut !<br>
                        Ceci est un message de Devloweb,<br>
                        Apparemment tu souhaite réinitialiser ton mot de passe !<br>
                        Clique sur ce lien pour le réinitialiser : <a href="https://{server_name}/reset_password?code={code}&email={email}">Réinitialiser !</a><br>
                        Et voici le code : <span style="font-weight: bold;">{code}</span><br>
                        Si tu n'es pas à l'origine de cette demande, répond à ce mail !
                    </p>
                  </body>
                </html>
                """
        html = html.format(code=code, email=target, server_name=os.environ['SERVER_NAME'])
        self.send_mail(text, html, message, target)

    def send_mail(self, text, html, message, target):
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP_SSL(self.host, self.port, context=self.context) as server:
            server.login(self.sender, self.app_pass)
            server.sendmail(self.sender, target, message.as_string())



