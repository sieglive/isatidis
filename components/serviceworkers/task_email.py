# coding:utf-8
"""PDF interface module"""
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
import traceback

from jinja2 import Environment, PackageLoader

from workers.manager import APP as app


@app.task
def send_email(subject, receivers, template_path, **values):
    """public email function."""
    mail_host = "mail.wondershare.com"
    mail_user = "esign@insidews.wondershare.com"
    mail_pass = "UCV3G85t3jp5a"
    env = Environment(loader=PackageLoader('workers', 'templates'))

    template = env.get_template(template_path)
    content = template.render(**values)
    sender = 'esign@insidews.wondershare.com'

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = f'Wondershare eSign+ <{sender}>'
    message['To'] = ','.join(receivers)
    message['subject'] = Header(subject, 'utf-8')
    message['Accept-Language'] = 'zh-CN'
    message['Accept-Charset'] = 'ISO-8859-1, utf-8'

    for _ in range(5):
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(mail_host, 25)
            smtp_obj.login(mail_user, mail_pass)
            smtp_obj.sendmail(sender, receivers, message.as_string())
            smtp_obj.quit()
            break
        except ConnectionRefusedError as exception:
            traceback.print_exc()
            return dict(
                result=0,
                status=1,
                msg='Connection refused when sending email.',
                exc_doc=str(exception))
        except TimeoutError as exception:
            return dict(
                result=0,
                status=1,
                msg='Connect email server time out.',
                data=dict(
                    exc_doc=str(exception),
                    output_html=content))
        time.sleep(1)

    return dict(
        result=1,
        status=0,
        msg='Send email successfully.',
        data=values)


def test():
    """test function."""
    this_subject = 'Python SMTP 邮件测试'
    this_receivers = ['314624180@qq.com']

    send_email(
        subject=this_subject,
        receivers=this_receivers,
        template_path='email/activeEmail.html',
        base_url='10.11.0.80',
        base_static_url='//10.11.0.80/static',
        email_address='sieglive@163.com', )


if __name__ == '__main__':
    test()
