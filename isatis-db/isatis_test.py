# coding:utf-8

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.utils import formatdate
from email.header import Header


smtpserver = 'smtp.exmail.qq.com'

subject = 'Test Isatidis Account'
body = 'Testllllllllllllllll'

mail = MIMEText(body.encode(), 'plain', 'utf-8')
mail['Subject'] = Header(subject, 'utf-8')
mail['From'] = 'account@isatidis.cn'
mail['To'] = '314624180@qq.com'
mail['Date'] = formatdate()


smtp_server = SMTP_SSL(smtpserver, 465)
smtp_server.set_debuglevel(1)
smtp_server.ehlo()
smtp_server.login('account@isatidis.cn', 'Siegfried1314~~~')
smtp_server.sendmail('account@isatidis.cn', ['314624180@qq.com'], mail.as_string())
smtp_server.close()


