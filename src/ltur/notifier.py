# -*- coding: utf-8 -*-

import sys

from config_parser import ConfigParser
from scrapers import LturScraper


class LturNotifier:

    def __init__(self, config_file):
        self.config_file = config_file

    def run(self):
        config = ConfigParser(self.config_file)

        scraper = LturScraper(origin=config.from_city(), destination=config.to_city(),
                              travel_datetime=config.departure_datetime())

        journeys = scraper.scrape_journeys()
        cheap_journeys = self._filter_cheap_journeys(journeys, config)
        content = config.output_formatter().format(cheap_journeys)

        config.target_publisher().publish(scraper.title(), content)

    def _filter_cheap_journeys(self, all_found_journeys, config):
        return filter(lambda it: it.special_price <= config.max_price(), all_found_journeys)


if __name__ == '__main__':
    notifier = LturNotifier(sys.argv[1])
    notifier.run()
