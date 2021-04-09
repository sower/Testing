from email.encoders import encode_base64
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import smtplib
import requests
import time
import math


def query():
    url = 'https://api.shuax.com/v2/chrome'
    response = requests.post(url)
    data = response.json()['win_stable_x64']
    chrome = {}
    chrome['update_time'] = math.floor(
        (time.time()*1000 - data['time'])/86400000)
    chrome['size'] = round(data['size'] / 1024 ** 2, 2)
    chrome['version'] = data['version']
    chrome['download_url'] = data['urls'][4]
    print(chrome)

    with open('log.txt', 'r', encoding='utf-8') as f:
        if f.read() == chrome['version']:
            return False

    with open('log.txt', 'w', encoding='utf-8') as f:
        f.write(chrome['version'])
        return chrome


class Mail():
    def __init__(self, user, pwd, host):
        self.mail_user = user
        self.mail_pwd = pwd      # 邮箱授权码
        self.mail_server = smtplib.SMTP()
        self.mail_server.connect(host, 25)
        self.mail_server.ehlo()
        self.mail_server.login(self.mail_user, self.mail_pwd)

    def __del__(self):
        self.mail_server.close()

    # 发送邮件
    def send_mail(self, recipient, subject, text, file_path=None):
        msg = MIMEMultipart()
        msg["From"] = self.mail_user
        msg["Subject"] = subject
        msg["To"] = ",".join(recipient)
        msg.attach(MIMEText(text))
        if file_path:
            msg.attach(self.get_attachment(file_path))
        self.mail_server.sendmail(self.mail_user, recipient, msg.as_string())
        print("——邮件发送成功——")

    # 添加邮件附件
    def get_attachment(self, file_path):
        file_name = file_path.split("\\")[-1]
        attachment = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        # attachment["Content-Type"] = 'application/octet-stream'
        attachment["Content-Disposition"] = 'attachment; filename=' + file_name
        return attachment


if __name__ == '__main__':
    chrome = query()
    if chrome:
        title = "Chrome Update Notification"
        content = f"""
            Chrome had Update!
            GUI url: {'https://tools.shuax.com/chrome/'}
            latest version: {chrome['version']}
            File size: {chrome['size']} MB
            Updated: {chrome['update_time']}天前
            download link: {chrome['download_url']}
        """
        with open(r'result.html', 'w', encoding='utf-8') as f:
            f.write(content)
