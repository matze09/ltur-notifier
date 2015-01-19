#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import httplib
import urllib
import sys
import re

from mechanize import Browser
from bs4 import BeautifulSoup

from conf.config import *
from conf.settings import *

# TODO: error handling
# (1) if on_date - today > 7, inform user


def main():
    page = submit_form()
    prices = parse_page(page.read(), TRIGGER)
    if any([p <= max_price for p in prices]):
        print OUTPUT_FORMAT.format(prices)


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


def parse_page(haystack, needles):
    bs = BeautifulSoup(haystack)
    gems = []
    price_tags = []
    for needle in needles:
        price_tags.extend(bs.find_all('td', attrs={'class': needle}))

    for price_tag in price_tags:
        price_string = price_tag.get_text().strip()
        match = re.match(PRICE_TAG_REGEX, unicode(price_string))
        if match:
            price = match.group(1)
            price = re.sub(',', '.', price)
            gems.append(float(price))
    return gems


if __name__ == '__main__':
    main()
