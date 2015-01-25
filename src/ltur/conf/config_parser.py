__author__ = 'mloeks'

import imp
from datetime import datetime, timedelta

from ltur.exceptions import *


class ConfigParser:

    def __init__(self, config_file):
        self.config_file = config_file

        self.config = self._parse_config()

    def _parse_config(self):
        return imp.load_source('ltur.config', self.config_file)

    def from_city(self):
        return self.config.from_city

    def to_city(self):
        return self.config.to_city

    def departure_datetime(self):
        return self._parse_config_datetime()

    def max_price(self):
        return self.config.max_price

    def output_formatter(self):
        return self.config.OUTPUT_FORMAT

    def target_publisher(self):
        return self.config.PUBLISH_TARGET

    def raw_config(self):
        return self.config

    def _parse_config_datetime(self):
        datetime_parser = ConfigDatetimeParser(self.config.at_date, self.config.at_time)
        return datetime_parser.get_datetime()


class ConfigDatetimeParser:

    def __init__(self, config_date, config_time):
        self.config_date = config_date
        self.config_time = config_time

    def get_datetime(self):
        travel_time = self._parse_config_time(self.config_time)
        travel_date = self._parse_config_date(self.config_date)
        return datetime.combine(travel_date, travel_time)

    def _parse_config_time(self, input_time):
        try:
            return datetime.strptime(input_time, '%H:%M').time()
        except ValueError:
            raise MalformedConfigError("Failed to parse travel_time [%s] from config. Please specify time in HH:MM "
                                       "24h format!" % input_time)

    def _parse_config_date(self, input_date):
        parsed_date = self._parse_config_date_datestring(str(input_date))
        if not parsed_date:
            parsed_date = self._parse_config_date_futuredays(input_date)
        if not parsed_date:
            parsed_date = self._parse_config_date_weekday(str(input_date))

        if not parsed_date:
            raise MalformedConfigError("Failed to parse travel date '%s' from config. Please specify either a"
                                       "date in format DD-MM-YYYY, a number of days between 0 and 7 to add to today "
                                       "(e.g. '2') or a weekday name (e.g. 'Saturday')" % input_date)
        return parsed_date

    def _parse_config_date_datestring(self, input_date):
        try:
            parsed_date = datetime.strptime(input_date, '%d-%m-%Y').date()
            diff_today = (parsed_date - datetime.now().date()).days
            if not 0 <= diff_today <= 7:
                raise MalformedConfigError("The travel date must not be more than 7 days ahead (%i specified)."
                                           % diff_today)
            return parsed_date
        except ValueError:
            return None

    def _parse_config_date_futuredays(self, input_date):
        try:
            days_to_add = int(input_date)
            if 0 <= days_to_add <= 7:
                return (datetime.now() + timedelta(days=days_to_add)).date()
            else:
                raise MalformedConfigError("The travel date must not be more than 7 days ahead (%i specified)."
                                           % days_to_add)
        except ValueError:
            return None

    def _parse_config_date_weekday(self, input_date):
        try:
            parsed_date = datetime.now().date()
            while 0 <= (parsed_date - datetime.now().date()).days <= 7:
                if parsed_date.strftime('%A') == input_date:
                    return parsed_date
                parsed_date = parsed_date + timedelta(days=1)
        except ValueError:
            return None
