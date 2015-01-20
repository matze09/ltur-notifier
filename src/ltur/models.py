# -*- coding: utf-8 -*-
__author__ = 'mloeks'

import math


class LturJourney:

    DATETIME_FORMAT = '%x %X'

    def __init__(self, origin, destination, departure, arrival, changes, special_price, regular_price):
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.changes = changes
        self.special_price = special_price
        self.regular_price = regular_price

    def _calculate_duration(self):
        return self.arrival - self.departure

    def _parse_from_html_tag(self):
        # TODO
        raise NotImplementedError

    def to_dict(self):
        return {
            'origin': unicode(self.origin),
            'destination': unicode(self.destination),
            'departure': self.departure,
            'arrival': self.arrival,
            'duration': self._calculate_duration(),
            'changes': self.changes,
            'special_price': self.special_price,
            'regular_price': self.regular_price
        }

    def __str__(self):
        duration_string = DateTimeFormattingUtils.duration_to_string(self._calculate_duration())
        return unicode("{orig} to {dest} on {dep} -> {arr} - {dur} hrs - {changes} changes | "
                       "{special} EUR (instead of {normal} EUR)")\
            .format(orig=self.origin, dest=self.destination,
                    dep=self.departure.strftime(self.DATETIME_FORMAT), arr=self.arrival.strftime(self.DATETIME_FORMAT),
                    dur=duration_string, changes=self.changes,
                    special=self.special_price, normal=self.regular_price)


class DateTimeFormattingUtils:

    @staticmethod
    def duration_to_string(input_td):
        hrs = int(math.floor(input_td.seconds/3600.0))
        mins = int(math.floor((input_td.seconds - 3600.0*hrs)/60.0))

        hrs_string = str(hrs).zfill(2)
        mins_string = str(mins).zfill(2)

        return "%s:%s" % (hrs_string, mins_string)


