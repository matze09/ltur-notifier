# -*- coding: utf-8 -*-
__author__ = 'mloeks'

from abc import ABCMeta, abstractmethod, abstractproperty

import json
import datetime


class BaseFormatter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def format(self, journeys):
        """ Format a list of LTUR journeys. """


class TextFormatter(BaseFormatter):

    def format(self, journeys):
        return "\n".join([unicode(journey) for journey in journeys])


class JsonFormatter(BaseFormatter):

    def __init__(self, pretty_print=False):
        self.pretty_print = pretty_print

    def format(self, journeys):
        output_list = []
        for journey in journeys:
            journey_dict = journey.to_dict()
            print journey_dict
            journey_dict = self._format_datetimes_for_json(journey_dict)
            output_list.append(journey_dict)

        if self.pretty_print:
            return json.dumps(output_list, ensure_ascii=False, encoding='utf8', indent=4)
        else:
            return json.dumps(output_list, ensure_ascii=False, encoding='utf8')

    def _format_datetimes_for_json(self, journey_dict):
        for key, value in journey_dict.iteritems():
            if isinstance(value, datetime.datetime):
                journey_dict[key] = value.isoformat()
            elif isinstance(value, datetime.timedelta):
                journey_dict[key] = value.total_seconds()
            elif isinstance(value, unicode):
                journey_dict[key] = value.encode('utf-8')

        return journey_dict


class HtmlFormatter(BaseFormatter):

    def format(self, journeys):
        raise NotImplementedError
