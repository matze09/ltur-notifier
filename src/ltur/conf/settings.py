# -*- coding: utf-8 *-*

# ltur's Bahn webpage: journey form (dynamically loaded after page load via AJAX)
user_url = 'http://www.ltur.com/de/bahn.html?omnin=DB-DE'
scraper_url = 'http://bahn.ltur.com/ltb/searchform/external'

# keywords for webscraping
TRIGGER = [
    'price_Fernweh_H',      # really cheap prices
    'price_Sparpreis_H'     # medium cheap prices...
]
PRICE_TAG_REGEX = u'([0-9]{1,3}(,|.)?([0-9]{1,2}))?\s*€?'

