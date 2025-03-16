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
        self.app_pass = os.environ['SMTP_PASSWORD']
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



    def send_host_demand_acceptation_mail(self, target):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Site accepté"
        message["From"] = self.sender
        message["To"] = target

        text = """\
                Ceci est un message de Devloweb"""
        text = text.format()


        html = """\
                <html>
                  <body>
                    <p>Salut !<br>
                        Ceci est un message de Devloweb,<br>
                        Le site de ta JA a été accepté par un administrateur !<br>
                        Il est disponible à : <a href="https://{server_name}/reset_password?code={code}&email={email}">Réinitialiser !</a><br>
                    </p>
                  </body>
                </html>
                """
        html = html.format(email=target, server_name=os.environ['SERVER_NAME'])


        self.send_mail(text, html, message, target)

    def send_host_demand_reject_mail(self, target, reason):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Site rejeté"
        message["From"] = self.sender
        message["To"] = target

        text = """\
                Ceci est un message de Devloweb"""
        text = text.format(reason=reason)


        html = """\
                <html>
                  <body>
                    <p>Salut !<br>
                        Ceci est un message de Devloweb,<br>
                        Le site de ta JA a été refusé par un administrateur.<br>
                        Il a indiqué la raison suivante :<br>
                        {reason}
                    </p>
                  </body>
                </html>
                """
        html = html.format(reason=reason, email=target, server_name=os.environ['SERVER_NAME'])

        self.send_mail(text, html, message, target)

    def send_host_demand_accept_mail(self, target, link):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Site accepté"
        message["From"] = self.sender
        message["To"] = target

        text = """\
                       Ceci est un message de Devloweb"""
        text = text.format(link=link)

        html = """\
                       <html>
                         <body>
                           <p>Salut !<br>
                               Ceci est un message de Devloweb,<br>
                               Le site de ta JA a été accepté par un administrateur.<br>
                               Il est disponible à l'adresse suivante : <a href="{link}">{link}</a>
                           </p>
                         </body>
                       </html>
                       """
        html = html.format(link=link, email=target, server_name=os.environ['SERVER_NAME'])

        self.send_mail(text, html, message, target)