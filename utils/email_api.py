import smtplib
import ssl


class DevloMail:
    def __init__(self):
        self.host = 'smtp.gmail.com'
        self.port = 465
        self.sender = "devlowave.offi@gmail.com"
        self.app_pass = "hbbp gnba ftuf ijbt"
        self.context = ssl.create_default_context()

    def send_verification_email(self, target, code):
        message = """\
        Subject: Verification Devloweb
        
        Bonjour et bienvenue sur Devloweb,
        Voici votre code de vérification : """ + code
        with smtplib.SMTP_SSL(self.host, self.port, context=self.context) as server:
            server.login(self.sender, self.app_pass)
            server.sendmail(self.sender, target, message)



