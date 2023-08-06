import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Themail:

    def __init__(self,sender="python2developer@gmail.com",password="llzmfnztjvhnnlcs",smtp="smtp.gmail.com",port="465"):
        self.sender = sender
        self.password = password
        self.smtp = smtp
        self.port = port

    def send(self,receiver,subject,body):
        self.receiver = receiver
        self.subject = subject
        self.body = body

        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.sender
        message["To"] = self.receiver[0]
        message.attach(MIMEText(self.body, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp, self.port, context=context) as server:
            try:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.receiver, message.as_string())
            except Exception as err:
                return err

        return 'Success!'
