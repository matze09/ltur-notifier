# -*- encoding: utf-8 -*-
__author__ = 'mloeks'

from abc import ABCMeta, abstractmethod, abstractproperty

import smtplib
from email.mime.text import MIMEText

from ltur.conf.settings import user_url


class BasePublisher(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def publish(self, content):
        """ Publish formatted content to implemented targets. """


class ConsolePublisher(BasePublisher):

    def publish(self, content):
        if content:
            print content
        else:
            print "No journeys found."


class EmailPublisher(BasePublisher):

    def __init__(self, to_email, from_email, smtp_server, smtp_user, smtp_pass):
        self.to_email = to_email
        self.from_email = from_email
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass

    def publish(self, content):
        if content:
            msg = MIMEText("Ltur notification.\n Prices:\n%s €\n\n%s" % (content, user_url))
            msg['Subject'] = 'Ltur notifier'
            msg['From'] = self.from_email
            msg['To'] = self.to_email

            s = smtplib.SMTP(self.smtp_server)
            if self.smtp_user and self.smtp_pass:
                s.login(self.smtp_user, self.smtp_pass)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            s.quit()
        else:
            # TODO log debug
            print "No journeys found, thus no e-mail was sent."


class PushoverPublisher(BasePublisher):

    def publish(self, content):
        raise NotImplementedError

    # TODO
    # def send_pushover(cheapest):
    #     if not USER_TOKEN:
    #         print( "You have to configure your Pushover user token in config.py for this to work." )
    #         sys.exit()
    #         conn = httplib.HTTPSConnection(PUSHOVER_URL)
    #         conn.request('POST', PUSHOVER_PATH,
    #                      urllib.urlencode({
    #                          'title': '( : ltur für ' + str(cheapest) + ' ',
    #                          'token': APP_TOKEN,
    #                          'user': USER_TOKEN,
    #                          'message': ')',
    #                          }), {'Content-type': 'application/x-www-form-urlencoded'})
    #
    #         # for debugging
    #         res = conn.getresponse()
    #         conn.close()
