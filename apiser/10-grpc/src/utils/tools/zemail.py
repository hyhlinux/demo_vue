import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
try:
    from src.config import CONFIG
except ImportError:
    class CONFIG:
        EMAIL = {
            "user": os.getenv('EMAIL_USER', ""),
            "passwd": os.getenv("EMAIL_USER_PASSWD", ""),
        }

class SendEmail(object):
    hosts = "smtp.exmail.qq.com"
    host_port = 465

    def __init__(self, user_email, user_pwd, tls=False):
        print("conf:", user_email, user_pwd)
        self.user = user_email
        self.user_pass = user_pwd
        self.server = smtplib.SMTP_SSL(host=SendEmail.hosts, port=SendEmail.host_port)
        self.server.debuglevel = 1
        self.server.ehlo()
        if tls:
            self.server.starttls()


    def login(self):
        self.server = smtplib.SMTP_SSL(host=SendEmail.hosts, port=SendEmail.host_port)
        self.server.ehlo()
        self.server.login(self.user, self.user_pass)

    def sendEmail(self, to, msg):
        try:
            msg = self.body(msg=msg)
            self.login()  # 括号中对应的是发件人邮箱账号、邮箱密码
            self.server.sendmail(from_addr=self.user, to_addrs=to,  msg=msg)  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            self.logout()  # 关闭连接
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(e)

    def body(self, subject=None, msg=None):
        msg = MIMEText(msg, 'html', 'utf-8')
        msg['From'] = formataddr(["FromTES", self.user])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        if not subject:
            subject = '邮件激活'
        msg['Subject'] = subject
        return msg.as_string()

    def logout(self):
        self.server.quit()


Zemail = SendEmail(CONFIG.EMAIL.get("user"), CONFIG.EMAIL.get("passwd"))

def main():
    Zemail.sendEmail("2285020853@qq.com", "")

if __name__ == '__main__':
    main()
