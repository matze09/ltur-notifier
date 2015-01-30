# -*- coding: utf-8 -*-
__author__ = 'mloeks'

import unittest
import datetime
from datetime import timedelta

from ltur.models import LturJourney, DateTimeFormattingUtils


class TestModels(unittest.TestCase):

    def setUp(self):
        test_departure = datetime.datetime(2014, 1, 10, 20, 15)
        test_arrival = datetime.datetime(2014, 1, 11, 0, 25)
        self.test_journey = LturJourney(departure=test_departure, arrival=test_arrival, changes=2,
                                        special_price=17, regular_price=129.99, direct_link='http://www.example.com')

    def test_journey_to_dict(self):
        actual_output = self.test_journey.to_dict()

        self.assertEquals(self.test_journey.departure, actual_output['departure'])
        self.assertEquals(self.test_journey.arrival, actual_output['arrival'])
        self.assertEquals(timedelta(hours=4, minutes=10), actual_output['duration'])
        self.assertEquals(2, actual_output['changes'])
        self.assertEquals(17, actual_output['special_price'])
        self.assertEquals(129.99, actual_output['regular_price'])
        self.assertEquals('http://www.example.com', actual_output['direct_link'])

    def test_journey_to_string(self):
        expected_output = u"{dep} -> {arr} - 04:10 hrs - 2 changes " \
                          u"| 17.00 EUR (instead of 129.99 EUR) - http://www.example.com"\
            .format(dep=self.test_journey.departure.strftime(LturJourney.DATETIME_FORMAT),
                    arr=self.test_journey.arrival.strftime(LturJourney.DATETIME_FORMAT)
        )

        self.assertEquals(expected_output, unicode(self.test_journey))


class TestDateTimeFormattingUtils(unittest.TestCase):

    def test_timedelta_to_string(self):
        self.assertEquals('01:53', DateTimeFormattingUtils.duration_to_string(timedelta(seconds=6789)))


if __name__ == '__main__':
    unittest.main()