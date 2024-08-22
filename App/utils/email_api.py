import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DevloMail:
    def __init__(self):
        self.host = 'smtp.gmail.com'
        self.port = 465
        self.sender = "devlowave.offi@gmail.com"
        self.app_pass = "hbbp gnba ftuf ijbt"
        self.context = ssl.create_default_context()

    def send_verification_email(self, target, code):
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
                Afin d'activer ton compte voici le code : {code}.<br>
                <a href="https://devloweb.fr/verification">Vérifier ici !</a>
            </p>
          </body>
        </html>
        """
        html = html.format(code=code)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP_SSL(self.host, self.port, context=self.context) as server:
            server.login(self.sender, self.app_pass)
            server.sendmail(self.sender, target, message.as_string())

    def send_magic_link(self, target, code):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Réinitialisation du mot de passe"
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
                        Afin d'activer ton compte voici le code : {code}.<br>
                        <a href="https://devloweb.fr/verification">Vérifier ici !</a>
                    </p>
                  </body>
                </html>
                """
        html = html.format(code=code)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP_SSL(self.host, self.port, context=self.context) as server:
            server.login(self.sender, self.app_pass)
            server.sendmail(self.sender, target, message.as_string())



