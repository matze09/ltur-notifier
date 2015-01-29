# -*- coding: utf-8 -*-
__author__ = 'mloeks'

from abc import ABCMeta, abstractmethod, abstractproperty

import json
from datetime import datetime, timedelta
from jinja2 import Environment, PackageLoader

from ltur.models import DateTimeFormattingUtils


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
            journey_dict = self._format_datetimes_for_json(journey_dict)
            output_list.append(journey_dict)

        if self.pretty_print:
            return json.dumps(output_list, ensure_ascii=False, encoding='utf8', indent=4)
        else:
            return json.dumps(output_list, ensure_ascii=False, encoding='utf8')

    def _format_datetimes_for_json(self, journey_dict):
        for key, value in journey_dict.iteritems():
            if isinstance(value, datetime):
                journey_dict[key] = value.isoformat()
            elif isinstance(value, timedelta):
                journey_dict[key] = value.total_seconds()
            elif isinstance(value, unicode):
                journey_dict[key] = value.encode('utf-8')

        return journey_dict


class HtmlFormatter(BaseFormatter):

    def __init__(self):
        self.env = Environment(loader=PackageLoader('ltur', 'templates'))
        self._add_custom_jinja_filters(self.env)

    def format(self, journeys):
        template = self.env.get_template('journeys_template.html')
        return template.render(journeys=journeys)

    def _add_custom_jinja_filters(self, jinja_env):
        jinja_env.filters['datetime'] = self._output_datetime_format_filter
        jinja_env.filters['duration'] = self._output_duration_format_filter

    def _output_datetime_format_filter(self, datetime_value):
        return datetime_value.strftime('%d %b, %H:%M')

    def _output_duration_format_filter(self, timedelta_value):
        return DateTimeFormattingUtils.duration_to_string(timedelta_value)

