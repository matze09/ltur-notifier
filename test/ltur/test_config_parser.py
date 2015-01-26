# -*- coding: utf-8 -*-
__author__ = 'mloeks'

import os
import unittest
from datetime import datetime, timedelta

from ltur.config_parser import ConfigParser, ConfigDatetimeParser
from ltur.formatters import JsonFormatter
from ltur.publishers import ConsolePublisher
from ltur.exceptions import *


class TestConfigParser(unittest.TestCase):

    def setUp(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def test_parse_config(self):
        test_config_file = self.BASE_DIR + '/../../data/test/test_config.py'
        config = ConfigParser(test_config_file)

        self.assertEquals('Berlin Hbf', config.from_city())
        # self.assertEquals('Hamburg Hbf', config.to_city())
        self.assertEquals('Köln Hbf', config.to_city())
        self.assertEquals(40, config.max_price())
        self.assertTrue(isinstance(config.target_publisher(), ConsolePublisher))

        days_future = config.raw_config().at_date
        future_date = datetime.now().date() + timedelta(days=days_future)

        self.assertEquals(3, days_future)
        self.assertEquals('09:12', config.raw_config().at_time)
        self.assertEquals('%s 09:12:00' % str(future_date), str(config.departure_datetime()))


class TestConfigDatetimeParser(unittest.TestCase):

    def test_get_datetime_string(self):
        test_date = datetime.now().date() + timedelta(days=3)
        datetime_parser = ConfigDatetimeParser(test_date.strftime('%d-%m-%Y'), '15:30')
        parsed_datetime = datetime_parser.get_datetime()

        self.assertEquals('%s 15:30:00' % test_date.strftime('%Y-%m-%d'), str(parsed_datetime))

    def test_get_datetime_string_invalid(self):
        datetime_parser = ConfigDatetimeParser('32-13-2000', '15:30')
        self.assertRaises(MalformedConfigError, datetime_parser.get_datetime)

    def test_get_datetime_future_days(self):
        datetime_parser = ConfigDatetimeParser(3, '15:30')
        parsed_datetime = datetime_parser.get_datetime()

        expected_date = datetime.now().date() + timedelta(days=3)

        self.assertEquals('%s 15:30:00' % expected_date, str(parsed_datetime))

    def test_get_datetime_future_days_invalid(self):
        datetime_parser = ConfigDatetimeParser(8, '15:30')
        self.assertRaises(MalformedConfigError, datetime_parser.get_datetime)

    def test_get_datetime_weekday(self):
        test_weekday = 'Sunday'
        datetime_parser = ConfigDatetimeParser(test_weekday, '15:30')
        parsed_datetime = datetime_parser.get_datetime()

        self.assertEquals(test_weekday, parsed_datetime.strftime('%A'))
        self.assertTrue(0 <= (parsed_datetime.date() - datetime.now().date()).days <= 7)

    def test_get_datetime_weekday_invalid(self):
        test_weekday = 'Funday'
        datetime_parser = ConfigDatetimeParser(test_weekday, '15:30')
        self.assertRaises(MalformedConfigError, datetime_parser.get_datetime)


if __name__ == '__main__':
    unittest.main()