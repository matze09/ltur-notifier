# -*- coding: utf-8 -*-
__author__ = 'mloeks'

from abc import ABCMeta, abstractmethod, abstractproperty

import smtplib
import logging
from email.mime.text import MIMEText


class BasePublisher(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def publish(self, title, content):
        """ Publish formatted content to implemented targets. """


class ConsolePublisher(BasePublisher):

    def publish(self, title, content):
        print title
        print "-"*66
        if content:
            print content
        else:
            print "No journeys found."


class EmailPublisher(BasePublisher):

    logger = logging.getLogger(__name__)

    def __init__(self, to_email, from_email, smtp_server, smtp_user, smtp_pass):
        self.to_email = to_email
        self.from_email = from_email
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass

    def publish(self, title, content):
        if content:
            msg = self._compose_mail(title, content)
            self._send_mail(msg)
        else:
            self.logger.warn("No journeys found, thus no e-mail was sent.")

    def _compose_mail(self, title, content):
        msg_prefix = ""
        msg_suffix = ""

        msg_text = "\n\n".join([msg_prefix, content.encode('utf-8'), msg_suffix])

        msg = MIMEText(_text=msg_text, _charset='utf-8')

        msg['Subject'] = title
        msg['From'] = self.from_email
        msg['To'] = self.to_email

        return msg

    def _send_mail(self, msg):
        s = smtplib.SMTP(self.smtp_server)
        if self.smtp_user and self.smtp_pass:
            s.login(self.smtp_user, self.smtp_pass)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()


class PushoverPublisher(BasePublisher):

    def publish(self, title, content):
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
