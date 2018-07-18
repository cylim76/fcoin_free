# -*- coding: utf-8 -*-
"""
Created on Sat May 26 13:59:17 2018

@author:
"""

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.mime.base import MIMEBase
import smtplib
import balance
import fees
from config import from_addr, password, to_addr, smtp_server, filename



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


balance.balance(filename=filename)
fees.print_report(filename=filename)

"""文本格式的邮件正文 msg
msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
"""

""" html格式的邮件的 正文 msg
msg = MIMEText('<html><body><h1>Hello</h1>' +
    '<p>send by <a href="http://www.baidu.com">Python</a>...</p>' +
    '</body></html>', 'html', 'utf-8')
"""

#"""带附件发送邮件的 msg
msg = MIMEMultipart()
#"""

msg['From'] = _format_addr('lucas  <%s>' % from_addr)
msg['To'] = _format_addr('lucas <%s>' % to_addr)
msg['Subject'] = Header('邮件标题 …', 'utf-8').encode()

f = open(filename, 'r')
msgcon = ''''''
while True:
    line = f.readline()
    msgcon += line.strip() + '\n'
    if not line:
        break
f.close()

# 带附件发送的 邮件正文是MIMEText:
msg.attach(MIMEText(msgcon, 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open(filename, 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('report', 'txt', filename=filename)
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename=filename)
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)



server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string() )
server.quit()
