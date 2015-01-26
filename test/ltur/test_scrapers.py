# -*- coding: utf-8 -*-
__author__ = 'mloeks'

import unittest
import os
from datetime import datetime, timedelta

from ltur.scrapers import LturScraper, LturJourneyRequestor, LturResultPageParser
from ltur.formatters import TextFormatter, JsonFormatter


class TestLturScraper(unittest.TestCase):

    def test_ltur_scraper_realdata(self):
        test_travel_datetime = datetime.now() + timedelta(days=5)
        ltur_scraper = LturScraper(origin='Stuttgart Hbf', destination='Kiel Hbf', travel_datetime=test_travel_datetime)
        journeys = ltur_scraper.scrape_journeys()

        test_formatter = TextFormatter()
        print test_formatter.format(journeys)

    def test_ltur_scraper_title(self):
        test_travel_datetime = datetime.now() + timedelta(days=5)
        ltur_scraper = LturScraper(origin='Stuttgart Hbf', destination='Kiel Hbf', travel_datetime=test_travel_datetime)

        expected_output = u"[ltur] - Special offers for Stuttgart Hbf -> Kiel Hbf on {dep}"\
            .format(dep=test_travel_datetime.strftime('%a %d/%m/%y'))

        self.assertEquals(expected_output, ltur_scraper.title())

class TestLturResultPageParser(unittest.TestCase):

    def setUp(self):
        self._set_base_dir()

    def _set_base_dir(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    def test_ltur_result_page_parser_testdata(self):
        test_result_page = self.BASE_DIR + '/data/test/test_resultpage.html'
        result_parser = LturResultPageParser(open(test_result_page).read())
        actual_journeys = result_parser.parse_journeys()

        expected_journeys_json = open(self.BASE_DIR + '/data/test/expected_testdata_journeys.json').read()
        actual_journeys_json = JsonFormatter().format(actual_journeys)

        self.assertEquals(expected_journeys_json, actual_journeys_json)


if __name__ == '__main__':
    unittest.main()