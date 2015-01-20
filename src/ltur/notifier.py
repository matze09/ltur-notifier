# -*- coding: utf-8 -*-

import httplib
import urllib
import sys
import re
import datetime

from mechanize import Browser
from bs4 import BeautifulSoup

from conf.config import *
from conf.settings import *

from ltur.models import LturJourney

# TODO: error handling
# (1) if on_date - today > 7, inform user


def main():
    results_page = submit_form()
    journeys = parse_journeys(results_page.read(), TRIGGER)
    cheap_journeys = _filter_cheap_journeys(journeys)
    content = OUTPUT_FORMAT.format(cheap_journeys)
    PUBLISH_TARGET.publish(content)


def submit_form():
    br = Browser()  # create browser instance
    response = br.open(scraper_url)  # load page

    # hack
    rp_data = response.get_data()
    rp_data = re.sub(r'<optgroup label=".+">', "", rp_data)  # replace all optgroup elements
    response.set_data(rp_data)
    br.set_response(response)
    # eohack

    br.select_form(name='form_spar_topz')

    # fill in custom values
    br['from'] = from_city
    br['to_spar'] = to_city
    br.form.find_control('fromDate').readonly = False
    br['fromDate'] = on_date
    br['fromTime'] = at_time

    return br.submit()


def parse_journeys(haystack, needles):
    bs = BeautifulSoup(haystack)
    journeys = []
    price_tags = []
    for needle in needles:
        price_tags.extend(bs.find_all('td', attrs={'class': needle}))

    for price_tag in price_tags:
        price_string = price_tag.get_text().strip()
        match = re.match(PRICE_TAG_REGEX, unicode(price_string))
        if match:
            price = match.group(1)
            price = re.sub(',', '.', price)

            # TODO parse proper departue/arrival dates, no. of changes and regular price
            on_date_datetime = datetime.datetime.strptime(on_date, '%d.%m.%Y')
            new_journey = LturJourney(origin=from_city, destination=to_city, departure=on_date_datetime,
                                      arrival=on_date_datetime, changes=0, special_price=float(price),
                                      regular_price=1000.0)
            journeys.append(new_journey)

    return journeys


def _filter_cheap_journeys(all_found_journeys):
    return filter(lambda it: it.special_price <= max_price, all_found_journeys)


if __name__ == '__main__':
    main()
