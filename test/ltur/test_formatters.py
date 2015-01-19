# -*- encoding: utf-8 -*-
__author__ = 'mloeks'

import unittest
import datetime
from datetime import timedelta
import copy

from ltur.models import LturJourney
from ltur.formatters import TextFormatter


class TestTextFormatter(unittest.TestCase):

    def test_journeys_to_text(self):
        test_departure = datetime.datetime(2014, 1, 10, 20, 15)
        test_arrival = datetime.datetime(2014, 1, 11, 0, 25)

        test_journey_1 = LturJourney(origin="Mars", destination="Earth",
                                     departure=test_departure, arrival=test_arrival, changes=2,
                                     special_price=17.99, normal_price=129.99)

        test_journey_2 = copy.copy(test_journey_1)
        test_journey_2.origin = "Castrop-Rauxel Hbf"
        test_journey_2.destination = "Darmstadt Hbf"
        test_journey_2.special_price = 27

        test_journeys = [test_journey_1, test_journey_2]

        formatter = TextFormatter()

        expected_output = u"""Mars to Earth on {dep} -> {arr} - 04:10 hrs - 2 changes | 17.99 EUR (instead of 129.99 EUR)
Castrop-Rauxel Hbf to Darmstadt Hbf on {dep} -> {arr} - 04:10 hrs - 2 changes | 27 EUR (instead of 129.99 EUR)"""\
            .format(dep=test_departure.strftime(LturJourney.DATETIME_FORMAT),
                    arr=test_arrival.strftime(LturJourney.DATETIME_FORMAT))

        self.assertEquals(expected_output, formatter.format(test_journeys))


if __name__ == '__main__':
    unittest.main()