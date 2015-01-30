# -*- coding: utf-8 -*-

import sys
import logging

from config_parser import ConfigParser
from scrapers import LturScraper


class LturNotifier:

    logger = logging.getLogger(__name__)

    def __init__(self, config_file):
        self.config_file = config_file

    def run(self):
        self.logger.info("Scraping LTUR journeys based on config file '%s'" % self.config_file)
        config = ConfigParser(self.config_file)

        scraper = LturScraper(origin=config.from_city(), destination=config.to_city(),
                              travel_datetime=config.departure_datetime())

        journeys = scraper.scrape_journeys()
        cheap_journeys = self._filter_cheap_journeys(journeys, config.max_price())

        self.logger.info("Publishing found journeys...")
        config.target_publisher().publish(scraper, cheap_journeys)

    def _filter_cheap_journeys(self, all_found_journeys, max_price):
        return filter(lambda it: it.special_price <= max_price, all_found_journeys)


if __name__ == '__main__':
    notifier = LturNotifier(sys.argv[1])
    notifier.run()
