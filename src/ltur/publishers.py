# -*- coding: utf-8 -*-
__author__ = 'mloeks'

from abc import ABCMeta, abstractmethod, abstractproperty

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ltur.formatters import TextFormatter, HtmlFormatter


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

    def __init__(self, to_emails, from_email, smtp_server, smtp_user, smtp_pass, allow_html=True):
        self.to_emails = to_emails
        self.from_email = from_email
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.allow_html = allow_html

    def publish(self, used_scraper, journeys):
        if journeys:
            msg = self._compose_mail(used_scraper, journeys)
            self._send_mail(msg)
            self.logger.info("Notification E-Mail was sent successfully.")
        else:
            self.logger.warn("No journeys found, thus no e-mail was sent.")

    def _compose_mail(self, used_scraper, journeys):
        msg = MIMEMultipart('alternative')

        msg['Subject'] = used_scraper.title()
        msg['From'] = self.from_email
        msg['To'] = ','.join(self.to_emails)

        self._attach_plaintext_part(msg, used_scraper, journeys)

        if self.allow_html:
            self._attach_html_part(msg, used_scraper, journeys)

        return msg

    def _attach_plaintext_part(self, msg, used_scraper, journeys):
        plain_text_msg = self._compose_plain_msg(used_scraper, journeys)
        plain_part = MIMEText(plain_text_msg, 'plain', 'utf-8')
        msg.attach(plain_part)

    def _attach_html_part(self, msg, used_scraper, journeys):
        html_msg = self._compose_html_msg(journeys)
        html_part = MIMEText(html_msg, 'html')
        msg.attach(html_part)

    def _compose_plain_msg(self, used_scraper, journeys):
        msg_prefix = used_scraper.title()
        msg_suffix = "Book now: %s" % used_scraper.USER_URL

        formatter = TextFormatter()
        formatted_journeys = formatter.format(journeys)
        msg_text = "\n\n".join([msg_prefix, formatted_journeys, msg_suffix])

        return msg_text

    def _compose_html_msg(self, journeys):
        formatter = HtmlFormatter()
        formatted_journeys = formatter.format(journeys)
        return formatted_journeys

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
