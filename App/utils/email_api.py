import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader



class DevloMail:
    def __init__(self):
        self.host = 'smtp.gmail.com'
        self.port = 465
        self.sender = "devlowave.offi@gmail.com"
        self.app_pass = "hbbp gnba ftuf ijbt"
        self.context = ssl.create_default_context()

    def send_verification_email(self, target, code, ja_id):
      
        loader = FileSystemLoader('./templates')

        env = Environment(
            loader = loader,
            autoescape=select_autoescape()
        )
        
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = self.sender
        message["To"] = target

        html = env.get_template("email.html").render(code=code, id=ja_id)
        
        content = MIMEText(html, "html")

        message.attach(content)

        with smtplib.SMTP_SSL(self.host, self.port, context=self.context) as server:
            server.login(self.sender, self.app_pass)
            server.sendmail(self.sender, target, message.as_string())



