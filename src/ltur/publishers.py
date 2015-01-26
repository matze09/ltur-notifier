# -*- coding: utf-8 -*-
__author__ = 'mloeks'

from abc import ABCMeta, abstractmethod, abstractproperty

import smtplib
import logging
from email.mime.text import MIMEText

from ltur.formatters import TextFormatter


class BasePublisher(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def publish(self, used_scraper, journeys):
        """ Publish given journeys to implemented targets. """


class ConsolePublisher(BasePublisher):

    logger = logging.getLogger(__name__)

    def publish(self, used_scraper, journeys):
        print used_scraper.title()
        print "-"*66

        formatter = TextFormatter()
        if journeys:
            print formatter.format(journeys)
        else:
            print "No journeys found."


class EmailPublisher(BasePublisher):

    logger = logging.getLogger(__name__)

    def __init__(self, to_emails, from_email, smtp_server, smtp_user, smtp_pass):
        self.to_emails = to_emails
        self.from_email = from_email
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass

    def publish(self, used_scraper, journeys):
        if journeys:
            msg = self._compose_mail(used_scraper, journeys)
            self._send_mail(msg)
            self.logger.info("Notification E-Mail was sent successfully.")
        else:
            self.logger.warn("No journeys found, thus no e-mail was sent.")

    def _compose_mail(self, used_scraper, journeys):
        msg_prefix = "Current special offers for %s" % used_scraper.title()
        msg_suffix = "Book now: %s" % used_scraper.USER_URL

        formatter = TextFormatter()
        formatted_journeys = formatter.format(journeys)
        msg_text = "\n\n".join([msg_prefix, formatted_journeys, msg_suffix])

        msg = MIMEText(_text=msg_text, _charset='utf-8')

        msg['Subject'] = used_scraper.title()
        msg['From'] = self.from_email
        msg['To'] = ','.join(self.to_emails)

        return msg

    def _send_mail(self, msg):
        s = smtplib.SMTP(self.smtp_server)
        if self.smtp_user and self.smtp_pass:
            s.login(self.smtp_user, self.smtp_pass)
        s.sendmail(msg['From'], self.to_emails, msg.as_string())
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
