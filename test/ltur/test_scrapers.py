# -*- coding: utf-8 -*-
__author__ = 'mloeks'

import unittest
from datetime import datetime, timedelta

from ltur.scrapers import LturScraper
from ltur.formatters import TextFormatter


class TestScrapers(unittest.TestCase):

    def test_ltur_scraper_realdata(self):
        test_travel_datetime = datetime.now() + timedelta(days=5)
        ltur_scraper = LturScraper(origin='Stuttgart Hbf', destination='Kiel Hbf', travel_datetime=test_travel_datetime)
        journeys = ltur_scraper.scrape_journeys()

        test_formatter = TextFormatter()
        print test_formatter.format(journeys)

    def test_ltur_scraper_testdata(self):
        raise NotImplementedError

    def test_ltur_scraper_title(self):
        test_travel_datetime = datetime.now() + timedelta(days=5)
        ltur_scraper = LturScraper(origin='Stuttgart Hbf', destination='Kiel Hbf', travel_datetime=test_travel_datetime)

        expected_output = u"[ltur] - Special offers for Stuttgart Hbf -> Kiel Hbf on {dep}"\
            .format(dep=test_travel_datetime.strftime(LturScraper.FORM_DATE_FORMAT))

        self.assertEquals(expected_output, ltur_scraper.title())


if __name__ == '__main__':
    unittest.main()