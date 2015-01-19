# -*- encoding: utf-8 *-*

import datetime

from ltur.formatters import TextFormatter, EmailFormatter, PushoverFormatter

# customize traveling specs
# mind that ltur offers bahn tickets only for the next 7 days starting from tomorrow
from_city = 'Berlin Hbf'
to_city = 'München Hbf'

# default to tomorrow
on_date = ( datetime.date.today() + datetime.timedelta( days=1 )).strftime( '%d.%m.%Y' )
#on_date = '21.01.2013'

at_time = '09:12'
max_price = 40.0

# set the output: pushover, email, text, ...
OUTPUT_FORMAT = TextFormatter()
# OUTPUT_FORMAT = EmailFormatter(
#     to_email='you@example.org', from_email='lturdaemon@example.org',
#     smtp_server='smtp.example.org', smtp_user='lturdaemon@example.org',
#     smtp_pass='somesecretpassword'
# )

# OUTPUT_FORMAT = PushoverFormatter()
# APP_TOKEN   = 'EpMD3BrlmxioeKvGujVccccPqHeUxd'
# USER_TOKEN  = ''
# PUSHOVER_URL = "api.pushover.net"
# PUSHOVER_PATH = "/1/messages.json"
