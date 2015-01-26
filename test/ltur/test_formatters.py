# -*- coding: utf-8 -*-
__author__ = 'mloeks'

import os
import unittest
import datetime
from datetime import timedelta
import copy

from ltur.models import LturJourney
from ltur.formatters import TextFormatter, JsonFormatter


class TestFormatters(unittest.TestCase):

    def setUp(self):
        self._set_base_dir()
        self._create_test_journeys()

    def _set_base_dir(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    def _create_test_journeys(self):
        test_departure = datetime.datetime(2014, 1, 10, 20, 15)
        test_arrival = datetime.datetime(2014, 1, 11, 0, 25)

        self.test_journey_1 = LturJourney(departure=test_departure, arrival=test_arrival, changes=2,
                                          special_price=17, regular_price=129.99)

        self.test_journey_2 = copy.copy(self.test_journey_1)
        self.test_journey_2.special_price = 27

        self.test_journeys = [self.test_journey_1, self.test_journey_2]

    def test_text_formatter(self):
        formatter = TextFormatter()

        expected_output = u"""{dep} -> {arr} - 04:10 hrs - 2 changes | 17.00 EUR (instead of 129.99 EUR)
{dep} -> {arr} - 04:10 hrs - 2 changes | 27.00 EUR (instead of 129.99 EUR)"""\
            .format(dep=self.test_journey_1.departure.strftime(LturJourney.DATETIME_FORMAT),
                    arr=self.test_journey_1.arrival.strftime(LturJourney.DATETIME_FORMAT))
        actual_output = formatter.format(self.test_journeys)

        self.assertEquals(expected_output, actual_output)

    def test_json_formatter(self):
        formatter = JsonFormatter()

        expected_output = open(self.BASE_DIR + '/data/test/expected.json').read()
        actual_output = formatter.format(self.test_journeys)

        self.assertEquals(expected_output.strip(), actual_output.strip())



if __name__ == '__main__':
    unittest.main()