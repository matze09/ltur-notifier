# -*- encoding: utf-8 -*-
__author__ = 'mloeks'

from abc import ABCMeta, abstractmethod, abstractproperty

import smtplib
from email.mime.text import MIMEText

from ltur.conf.settings import user_url


class BaseFormatter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def format(self, journeys):
        """ Format a list of LTUR journeys. """


class TextFormatter(BaseFormatter):

    def format(self, journeys):
        return "\n".join([str(journey) for journey in journeys])


class JsonFormatter(BaseFormatter):

    def format(self, journeys):
        raise NotImplementedError


class HtmlFormatter(BaseFormatter):

    def format(self, journeys):
        raise NotImplementedError
