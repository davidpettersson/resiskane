#
# network.py
#

from urllib2 import urlopen
from urllib import urlencode
from constants import BASE_URL

def send_req(page, params):
    return urlopen(BASE_URL % (page, urlencode(params))).read()


