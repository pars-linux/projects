#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from string import join

from blog_conf import *


class sendMail:
    From = BLOGMAILADDR
    Content = ''
    server = ''
    body = ''

    def __init__(self, From, Content):
        self.server = smtplib.SMTP(SMTPSERVER)
        if From: self.From = From
        if Content: self.Content = Content
        self.body = join((
                    "From: %s" % self.From,
                    "To: %s" % EMAIL,
                    "Subject: %s" % SITENAME,
                    "", 
		    self.Content), 
		    "\r\n")
        self.send()

    def send(self):
        try:
            self.server.sendmail(self.From, EMAIL, self.body)
            print "<p><center><hr><b>E-postanız gönderildi..</b><hr><center></p><br>"
        except:
            print "<p><center><hr><b>Bir hata oldu, ve e-posta gönderemedik :(</b><hr><center></p><br>"

