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
        message["Subject"] = "multipart test"
        message["From"] = self.sender
        message["To"] = target

        text = """\
        Hey comment tu vas voici ton super code : {code}"""
        text = text.format(code=code)

        html = """\
        <html>
          <body>
            <p>Hi,<br>
                How are you?<br>
                Voici ton code : {code}
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



