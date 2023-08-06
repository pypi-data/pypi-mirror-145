import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime


class Email():

    def __init__(self,**parameter):
        """
        初始化
        #文件名不要用因为
        :param parameter: 
        """""
        self.sender = parameter['sender']       #发送的邮件地址
        self.auth_code = parameter['auth_code'] #授权码，网页登陆QQ邮箱后，从「设置」-「账户」-「开启 POP3/SMTP服务」中获得
        self.receivers = parameter['receivers'] #接收邮件，可设置为你的QQ邮箱或者其他邮箱  #列表

    # 发送带附件的邮件邮件
    def post_resources_email(self, file_path, top_message ='默认开头', maintext="邮件正文"):
        sender = self.sender  # 邮箱地址
        auth_code = self.auth_code  # 授权码，网页登陆QQ邮箱后，从「设置」-「账户」-「开启 POP3/SMTP服务」中获得
        receivers = self.receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receivers[0]

        message['Subject'] = Header(f'{top_message}', 'utf-8')
        # 邮件正文内容
        message.attach(MIMEText(f'{maintext}', 'plain', 'utf-8'))
        # 构造附件1
        att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'

        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        filename = file_path.split("/")[-1]
        print(filename)
        att1["Content-Disposition"] = f"attachment; filename='{filename}'"
        message.attach(att1)
        with smtplib.SMTP_SSL("smtp.qq.com", 465) as smtp:
            smtp.login(sender, auth_code)  # 登陆邮箱
            smtp.sendmail(sender, receivers, message.as_string())
            print(f'发送邮件成功---{datetime.now()}')