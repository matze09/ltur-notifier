# -*- coding: utf-8 -*-
__author__ = 'mloeks'

from datetime import timedelta, datetime
from abc import ABCMeta, abstractmethod, abstractproperty
import re

from mechanize import Browser
from bs4 import BeautifulSoup

from exceptions import *
from models import LturJourney


class BaseScraper(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def scrape_journeys(self):
        """ Parse journeys from a certain website. """

    @abstractproperty
    def form_url(self):
        """ URL of the website/form where to put travel data in. """

    @abstractproperty
    def origin(self):
        """ Desired journey origin. """

    @abstractproperty
    def destination(self):
        """ Desired journey destination. """

    @abstractproperty
    def travel_datetime(self):
        """ Desired date and time of travel. """

    @abstractproperty
    def title(self):
        """ Descriptive title which will be displayed through publishers. """


class LturScraper(BaseScraper):

    # ltur's Bahn webpage: journey form (dynamically loaded after page load via AJAX)
    USER_URL = 'http://www.ltur.com/de/bahn.html?omnin=DB-DE'
    SCRAPER_URL = 'http://bahn.ltur.com/ltb/searchform/external'

    def __init__(self, origin, destination, travel_datetime):
        self._origin = origin
        self._destination = destination
        self._travel_datetime = travel_datetime

    def scrape_journeys(self):
        journey_requestor = LturJourneyRequestor(form_url=self.form_url(), origin=self.origin(),
                                                 destination=self.destination(), travel_datetime=self.travel_datetime())
        results_page = journey_requestor.get_result_page()

        result_page_parser = LturResultPageParser(result_page_html=results_page)
        return result_page_parser.parse_journeys()

    def form_url(self):
        return self.SCRAPER_URL

    def origin(self):
        return self._origin

    def destination(self):
        return self._destination

    def travel_datetime(self):
        return self._travel_datetime

    def title(self):
        title = '[ltur] - Special offers for %s -> %s on %s' % (self.origin(), self.destination(),
                                                                self.travel_datetime().strftime('%d/%m/%y'))
        return title


class LturJourneyRequestor:

    FORM_DATE_FORMAT = '%d.%m.%Y'
    FORM_TIME_FORMAT = '%H:%M'

    def __init__(self, form_url, origin, destination, travel_datetime):
        self.form_url = form_url
        self.origin = origin
        self.destination = destination
        self.travel_datetime = travel_datetime

    # TODO refactor
    def get_result_page(self):
        br = Browser()  # create browser instance
        response = br.open(self.form_url)  # load page

        # hack
        rp_data = response.get_data()
        rp_data = re.sub(r'<optgroup label=".+">', "", rp_data)  # replace all optgroup elements
        response.set_data(rp_data)
        br.set_response(response)
        # eohack

        br.select_form(name='form_spar_topz')

        # fill in custom values
        br['from'] = self.origin.encode('utf-8')
        br['to_spar'] = self.destination.encode('utf-8')
        br.form.find_control('fromDate').readonly = False
        br['fromDate'] = self.travel_datetime.strftime(self.FORM_DATE_FORMAT)
        br['fromTime'] = self.travel_datetime.strftime(self.FORM_TIME_FORMAT)

        return br.submit()


class LturResultPageParser:

    # keywords for webscraping
    TRIGGER = [
        'price_Fernweh_H',      # really cheap prices
        'price_Sparpreis_H'     # medium cheap prices...
    ]
    PRICE_TAG_REGEX = u'([0-9]{1,3}(,|.)?([0-9]{1,2}))?\s*€?'

    def __init__(self, result_page_html):
        self.result_page_html = result_page_html

    def parse_journeys(self):
        bs = BeautifulSoup(self.result_page_html)
        journeys = []
        price_tags = []
        for needle in self.TRIGGER:
            price_tags.extend(bs.find_all('td', attrs={'class': needle}))

        for price_tag in price_tags:
            price_string = price_tag.get_text().strip()
            match = re.match(self.PRICE_TAG_REGEX, unicode(price_string))
            if match:
                price = match.group(1)
                price = re.sub(',', '.', price)

                # TODO parse proper departure/arrival dates, no. of changes and regular price (currently faked)
                on_date_datetime = datetime.now()
                new_journey = LturJourney(departure=on_date_datetime, arrival=on_date_datetime, changes=0,
                                          special_price=float(price), regular_price=1000.0)
                journeys.append(new_journey)

        return journeys