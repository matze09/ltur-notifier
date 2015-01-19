__author__ = 'mloeks'

import unittest
import datetime
from datetime import timedelta

from ltur.models import LturJourney, DateTimeFormattingUtils


class TestModels(unittest.TestCase):

    def test_journey_to_string(self):
        test_departure = datetime.datetime(2014, 1, 10, 20, 15)
        test_arrival = datetime.datetime(2014, 1, 11, 0, 25)
        test_journey = LturJourney(origin="Mars", destination="Earth",
                                   departure=test_departure, arrival=test_arrival, changes=2,
                                   special_price=17.99, normal_price=129.99)

        expected_output = u"Mars to Earth on {dep} -> {arr} - 04:10 hrs - 2 changes " \
                          u"| 17.99 EUR (instead of 129.99 EUR)"\
            .format(dep=test_departure.strftime(LturJourney.DATETIME_FORMAT),
                    arr=test_arrival.strftime(LturJourney.DATETIME_FORMAT)
        )

        self.assertEquals(expected_output, str(test_journey))


class TestDateTimeFormattingUtils(unittest.TestCase):

    def test_timedelta_to_string(self):
        self.assertEquals('01:53', DateTimeFormattingUtils.duration_to_string(timedelta(seconds=6789)))


if __name__ == '__main__':
    unittest.main()