# -*- coding: utf-8 -*-
__author__ = 'mloeks'

from datetime import timedelta, datetime
from abc import ABCMeta, abstractmethod, abstractproperty
import re
import logging
from operator import attrgetter

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
    def user_url(self):
        """ URL of the website where the receiver should be guided to. """

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

    logger = logging.getLogger(__name__)

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

    def user_url(self):
        return self.USER_URL

    def origin(self):
        return self._origin

    def destination(self):
        return self._destination

    def travel_datetime(self):
        return self._travel_datetime

    def title(self):
        title = '[ltur] - Special offers for %s -> %s on %s' % (self.origin(), self.destination(),
                                                                self.travel_datetime().strftime('%a %d/%m/%y'))
        return title


class LturJourneyRequestor:

    FORM_DATE_FORMAT = '%d.%m.%Y'
    FORM_TIME_FORMAT = '%H:%M'

    logger = logging.getLogger(__name__)

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

    LTUR_DATE_FORMAT = '%d.%m'
    LTUR_TIME_FORMAT = '%H:%M'

    logger = logging.getLogger(__name__)

    def __init__(self, result_page_html):
        self.result_page_html = result_page_html

    def parse_journeys(self):
        bs = BeautifulSoup(self.result_page_html)
        journeys = []

        journey_trs = self._get_journey_trs(bs)

        for journey_tr in journey_trs:
            departure = self._get_departure_from_tr(journey_tr)
            arrival = self._get_arrival_from_tr(journey_tr)
            changes = self._get_changes_from_tr(journey_tr)
            special_price = self._get_special_price_from_tr(journey_tr)
            regular_price = self._get_regular_price_from_tr(journey_tr)
            direct_link = self._get_direct_link_from_tr(journey_tr)

            if special_price:
                new_journey = LturJourney(departure=departure, arrival=arrival, changes=changes,
                                          special_price=special_price, regular_price=regular_price,
                                          direct_link=direct_link)
                journeys.append(new_journey)

        sorted_journeys = sorted(journeys, key=attrgetter('departure', 'special_price', 'arrival', 'changes'))
        return sorted_journeys

    def _get_journey_trs(self, bs):
        rows = []
        for needle in self.TRIGGER:
            rows.extend(bs.find_all('td', attrs={'class': needle}))
        return [row.parent for row in rows]

    def _get_departure_from_tr(self, tr):
        cells = tr.find_all('td')

        date_td = list(cells)[1]
        time_td = list(cells)[2]

        dep_date = self._dates_from_td(date_td)[0]
        dep_time = self._times_from_td(time_td)[0]

        dep_date = dep_date.replace(year=datetime.now().year)

        return datetime.combine(dep_date, dep_time)

    def _get_arrival_from_tr(self, tr):
        cells = tr.find_all('td')

        date_td = list(cells)[1]
        time_td = list(cells)[2]

        dep_date = self._dates_from_td(date_td)[1]
        dep_time = self._times_from_td(time_td)[1]

        dep_date = dep_date.replace(year=datetime.now().year)

        return datetime.combine(dep_date, dep_time)

    def _dates_from_td(self, td):
        td_text = td.get_text()
        date_strings = re.findall('[0-9]{1,2}.[0-9]{1,2}', td_text)

        if len(date_strings) != 2:
            raise UnexpectedHtmlError('Error while parsing journey departure/arrival dates.')

        try:
            dates = [datetime.strptime(date, self.LTUR_DATE_FORMAT).date() for date in date_strings]
        except ValueError:
            raise UnexpectedHtmlError('Error while parsing journey departure/arrival dates. '
                                      'Date does not match expected format %s' % self.LTUR_DATE_FORMAT)
        return dates

    def _times_from_td(self, td):
        td_text = td.get_text()
        time_strings = re.findall('[0-9]{1,2}:[0-9]{1,2}', td_text)

        if len(time_strings) != 2:
            raise UnexpectedHtmlError('Error while parsing journey departure/arrival times.')

        try:
            times = [datetime.strptime(time, self.LTUR_TIME_FORMAT).time() for time in time_strings]
        except ValueError:
            raise UnexpectedHtmlError('Error while parsing journey departure/arrival times. '
                                      'Time does not match expected format %s' % self.LTUR_TIME_FORMAT)
        return times

    def _get_changes_from_tr(self, tr):
        td_changes = tr.find_next('td', attrs={'class': 'umstieg'})
        if not td_changes:
            raise UnexpectedHtmlError('Could not parse number of changes from result page.')

        return int(td_changes.get_text())

    def _get_special_price_from_tr(self, tr):
        td_special_prices = None

        for needle in self.TRIGGER:
            if not td_special_prices:
                td_special_prices = tr.find('td', {'class': needle}, recursive=False)

        if td_special_prices:
            match = re.match(self.PRICE_TAG_REGEX, unicode(td_special_prices.get_text().strip()))
            if match:
                price = match.group(1)
                price = re.sub(',', '.', price)
                return float(price)

        return None

    def _get_regular_price_from_tr(self, tr):
        td_regular_prices = tr.find('td', {'class': 'price_normH'}, recursive=False)

        if td_regular_prices:
            match = re.match(self.PRICE_TAG_REGEX, unicode(td_regular_prices.get_text().strip()))
            if match:
                price = match.group(1)
                price = re.sub(',', '.', price)
                return float(price)

        return None

    def _get_direct_link_from_tr(self, tr):
        # TODO implement parsing of direct booking link
        return 'http://www.ltur.com'
