# -*- coding: utf-8 *-*

import datetime

from ltur.formatters import TextFormatter, HtmlFormatter, JsonFormatter
from ltur.publishers import ConsolePublisher, EmailPublisher, PushoverPublisher

# customize traveling specs
# mind that ltur offers bahn tickets only for the next 7 days starting from tomorrow
from_city = "Berlin Hbf"
to_city = "Hamburg Hbf"

# departure date
at_date = 3               # default to tomorrow (+1 day)
# at_date = 'Tuesday'       # weekdays are also possible
# at_date = '25-01-2015'

at_time = '09:12'
max_price = 40.0

# set the output format: text, json, html ...
# OUTPUT_FORMAT = TextFormatter()
OUTPUT_FORMAT = JsonFormatter(pretty_print=True)

# set the destination to publish results: console, email, pushover ...
PUBLISH_TARGET = ConsolePublisher()

# PUBLISH_TARGET = EmailPublisher(
#     to_email='you@example.org', from_email='lturdaemon@example.org',
#     smtp_server='smtp.example.org', smtp_user='lturdaemon@example.org',
#     smtp_pass='somesecretpassword'
# )

# PUBLISH_TARGET = PushoverPublisher()
# APP_TOKEN   = 'EpMD3BrlmxioeKvGujVccccPqHeUxd'
# USER_TOKEN  = ''
# PUSHOVER_URL = "api.pushover.net"
# PUSHOVER_PATH = "/1/messages.json"
