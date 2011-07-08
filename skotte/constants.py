# -*- encoding: utf-8 -*-
#
# constants.py
#

NS = '{http://www.etis.fskab.se/v1.0/ETISws}'

TRANSPORT_MAP = {
    0: 'gång',
    1: 'stadsbuss',
    2: 'regionbuss',
    4: 'Skåneexpressen',
    8: 'Pendeln',
    16: 'Öresundståg',
    32: 'Pågatåg',
    64: 'tågbuss',
    128: 'färja',
}

BASE_URL = 'http://www.labs.skanetrafiken.se/v2.2/%s?%s'
