#
# mail_client.py
# @author yanchunhuo
# @description 
# @created 2023-10-07T17:01:27.872Z+08:00
# @last-modified 2024-01-15T14:55:14.840Z+08:00
#
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import smtplib

class MailClient:
    def __init__(self,pop3_host:str=None,pop3_port:int=None,smtp_host:str=None,smtp_port:int=None,mail:str=None,mail_password=None,
                 mail_from_name:str=None,is_ssl:bool=True) -> None:
        self.mail=mail
        self.mail_password=mail_password
        self.mail_from_name=mail_from_name
        if not smtp_host is None and not smtp_port is None:
            if is_ssl:
                self.smtp=smtplib.SMTP_SSL(smtp_host,smtp_port)
            else:
                self.smtp=smtplib.SMTP(smtp_host,smtp_port)
            self.smtp.login(mail,mail_password)
            
    def send_mail(self,to_mails:str,cc_mail:str=None,subject:str=None,content:str=None,is_content_html:bool=False,
                  attach_file_paths:list=None,attach_file_names:list=None):
        """_summary_

        Args:
            to_mails (str, 必填): 使用逗号隔开. Defaults to None.
            cc_mail (str, optional): 使用逗号隔开. Defaults to None.
            subject (str, optional): 主题. Defaults to None.
            content (str, optional): 文本内容. Defaults to None.
            is_content_html (bool, optional): 文本内容是否是html. Defaults to False.
            attach_file_paths (list, optional): 附件文件路径列表. Defaults to None.
            attach_file_names (list, optional): 附件文件名列表. Defaults to None.
        """
        message=MIMEMultipart()
        subject=Header(subject,'utf-8').encode()
        message['Subject']=subject
        if self.mail_from_name is None:
            message['From']=self.mail
        else:
            message['From']=formataddr(pair=(self.mail_from_name,self.mail))
        message['To']=to_mails
        message['Cc']=cc_mail
        if is_content_html:
            text=MIMEText(content,'html','utf-8')
        else:
            text=MIMEText(content,'plain','utf-8')
        message.attach(text)
        if not attach_file_paths is None:
            for i,attach_file_path in enumerate(attach_file_paths):
                attachment=MIMEText(open(attach_file_path,'rb').read(),'base64','utf-8')
                attachment["Content-Type"] = 'application/octet-stream'
                attachment.add_header("Content-Disposition", "attachment", filename=attach_file_names[i])
                message.attach(attachment)
        if not cc_mail is None:
            to_addrs=set(to_mails.split(',')).union(cc_mail.split(','))
        else:
            to_addrs=set(to_mails.split(','))
        self.smtp.sendmail(from_addr=self.mail,to_addrs=to_addrs,msg=message.as_string())
        
    def quit(self):
        self.smtp.close()