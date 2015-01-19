__author__ = 'mloeks'

import math


class LturJourney:

    DATETIME_FORMAT = '%x %X'

    def __init__(self, origin, destination, departure, arrival, changes, special_price, normal_price):
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.changes = changes
        self.special_price = special_price
        self.normal_price = normal_price

    def _calculate_duration(self):
        duration = self.arrival - self.departure
        return DateTimeFormattingUtils.duration_to_string(duration)

    def _parse_from_html_tag(self):
        # TODO
        raise NotImplementedError

    def __str__(self):
        return u"{orig} to {dest} on {dep} -> {arr} - {dur} hrs - {changes} changes | " \
               u"{special} EUR (instead of {normal} EUR)"\
            .format(orig=self.origin, dest=self.destination,
                    dep=self.departure.strftime(self.DATETIME_FORMAT), arr=self.arrival.strftime(self.DATETIME_FORMAT),
                    dur=self._calculate_duration(), changes=self.changes,
                    special=self.special_price, normal=self.normal_price)


class DateTimeFormattingUtils:

    @staticmethod
    def duration_to_string(input_td):
        hrs = int(math.floor(input_td.seconds/3600.0))
        mins = int(math.floor((input_td.seconds - 3600.0*hrs)/60.0))

        hrs_string = str(hrs).zfill(2)
        mins_string = str(mins).zfill(2)

        return "%s:%s" % (hrs_string, mins_string)


