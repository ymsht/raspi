#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
メールを扱うモジュール
"""

import sys
import smtplib
#import logging
#import logging.config
import datetime
import base64
import os
from email.MIMEText import MIMEText
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate
from email.Header import Header

class BaseMail():
    """
    メールを扱うクラス
    """
    
    def __init__(self):
        pass
        
    def send(self, msg, system_config):
        """
        メールを送信します。
        """
        smtp = smtplib.SMTP(system_config['smtp'], system_config['port'])
        smtp.login(system_config['user'], system_config['passwd'])
        to = system_config['to'].split(',')
        to.append(system_config['from'])
        smtp.sendmail(system_config['from'], to, msg.as_string())
        smtp.close()
        
    def create(self, subject, body, from_addr, to_addr, encoding):
        """
        メールを生成します。
        """
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, encoding)
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Date'] = formatdate()
        
        mail_body = MIMEText(body, 'plain', encoding)
        msg.attach(mail_body)
        
        return msg

    def create_message(self, subject, body, from_addr, to_addr, encoding, attachment_list):
        """
        添付ファイル付きメールを生成します。
        """
        msg = MIMEMultipart()
        msg['Subject'] = Header(subject, encoding)
        msg['From'] = from_addr
        msg['To'] = to_addr + ',' + from_addr
        msg['Date'] = formatdate()

        mail_body = MIMEText(body, 'plain', encoding)
        msg.attach(mail_body)

        for attach in attachment_list:
            if not os.path.isfile(attach[1]):
                #logging.warning(attach[1] + 'が存在しません。')
                continue
            with open(attach[1]) as f:
                csv = MIMEText(f.read(), 'plain', encoding)
                csv.add_header('Content-Disposition', 'attachment', filename=attach[0])
                msg.attach(csv)

        return msg
