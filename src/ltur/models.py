# -*- coding: utf-8 -*-
__author__ = 'mloeks'

import math


class LturJourney:

    DATETIME_FORMAT = '%d/%m %H:%M'

    def __init__(self, departure, arrival, changes, special_price, regular_price, direct_link):
        self.departure = departure
        self.arrival = arrival
        self.changes = changes
        self.special_price = special_price
        self.regular_price = regular_price
        self.direct_link = direct_link

    def _calculate_duration(self):
        return self.arrival - self.departure

    def to_dict(self):
        return {
            'departure': self.departure,
            'arrival': self.arrival,
            'duration': self._calculate_duration(),
            'changes': self.changes,
            'special_price': self.special_price,
            'regular_price': self.regular_price,
            'direct_link': self.direct_link
        }

    def __str__(self):
        duration_string = DateTimeFormattingUtils.duration_to_string(self._calculate_duration())
        return unicode("{dep} -> {arr} - {dur} hrs - {changes} changes | "
                       "{special} EUR (instead of {normal} EUR) - {link}")\
            .format(dep=self.departure.strftime(self.DATETIME_FORMAT), arr=self.arrival.strftime(self.DATETIME_FORMAT),
                    dur=duration_string, changes=self.changes,
                    special="%.2f" % self.special_price, normal="%.2f" % self.regular_price, link=self.direct_link)


class DateTimeFormattingUtils:

    @staticmethod
    def duration_to_string(input_td):
        hrs = int(math.floor(input_td.seconds/3600.0))
        mins = int(math.floor((input_td.seconds - 3600.0*hrs)/60.0))

        hrs_string = str(hrs).zfill(2)
        mins_string = str(mins).zfill(2)

        return "%s:%s" % (hrs_string, mins_string)


