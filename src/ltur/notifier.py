# -*- coding: utf-8 -*-

from conf.config_parser import ConfigParser
from ltur.scrapers import LturScraper


def main():
    # TODO config as cli parameter
    config = ConfigParser('conf/config.py')

    scraper = LturScraper(origin=config.from_city(), destination=config.to_city(),
                          travel_datetime=config.departure_datetime())

    journeys = scraper.scrape_journeys()
    cheap_journeys = _filter_cheap_journeys(journeys)
    content = config.output_formatter().format(cheap_journeys)
    config.target_publisher().publish(content)


def _filter_cheap_journeys(all_found_journeys):
    return filter(lambda it: it.special_price <= max_price, all_found_journeys)


if __name__ == '__main__':
    main()
