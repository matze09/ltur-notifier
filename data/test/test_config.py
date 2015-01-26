# -*- coding: utf-8 *-*

from ltur.publishers import ConsolePublisher, EmailPublisher, PushoverPublisher

# customize traveling specs
# mind that ltur offers bahn tickets only for the next 7 days starting from tomorrow
from_city = u"Stuttgart Hbf"
to_city = u"Köln Hbf"

# departure date
at_date = 5               # default to tomorrow (+1 day)
# at_date = 'Tuesday'       # weekdays are also possible
# at_date = '25-01-2015'

at_time = '09:12'
max_price = 40.0

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
