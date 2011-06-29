# -*- encoding: utf-8 -*-

from urllib2 import urlopen
from urllib import urlencode
from xml.dom.minidom import parseString
from xml.etree.ElementTree import ElementTree
from StringIO import StringIO
from pprint import pprint
from domain import Station, Journey, Link, Deviation
from datetime import datetime
from cache import get_station_cache, set_station_cache

def _build_url(page, params):
    return 'http://www.labs.skanetrafiken.se/v2.2/%s?%s' % (page, urlencode(params))

def _send_req(url):
    return urlopen(url).read()

def _as_text(ns):
    rc = [ ]
    for n in ns:
        if n.nodeType == n.TEXT_NODE:
            rc.append(n.data)
    return ''.join(rc)

def search_station(s):
    encoded_s = s.encode('utf-8')
    stations = get_station_cache(encoded_s)

    if stations:
        return stations

    url = _build_url('querystation.asp', { 'inpPointFr': encoded_s })
    body = _send_req(url)
    doc = parseString(body)
    Point_nodes = doc.getElementsByTagName('Point')
    stations = list()
    for element in Point_nodes:
        id_ = int(_as_text(element.getElementsByTagName('Id')[0].childNodes))
        name = _as_text(element.getElementsByTagName('Name')[0].childNodes)
        st = Station(id_, name)
        if not st in stations:
            stations.append(st)
    set_station_cache(encoded_s, stations)
    return stations

NS_ETISWS = '{http://www.etis.fskab.se/v1.0/ETISws}'

def _parse_date_time(ns, d):
    return datetime.strptime(d.text, '%Y-%m-%dT%H:%M:%S')

def _parse_station(ns, p):
    return Station(int(p.find(ns + 'Id').text),
                   p.find(ns + 'Name').text)

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

def _parse_transport_type(ns, l):
    tid = int(l.find(ns + 'LineTypeId').text)
    return TRANSPORT_MAP[tid]

def _parse_transport_name(ns, l):
    return l.find(ns + 'Name').text

def _parse_deviation(ns, d):
    return Deviation(d.find(ns + 'Header').text,
                     d.find(ns + 'Details').text)

def _parse_deviations(ns, ds):
    return [ _parse_deviation(ns, d) for d in ds.getchildren() ]

def _parse_route_link(ns, r):
    return Link(_parse_date_time(ns, r.find(ns + 'DepDateTime')),
                _parse_station(ns, r.find(ns + 'From')),
                _parse_date_time(ns, r.find(ns + 'ArrDateTime')),
                _parse_station(ns, r.find(ns + 'To')),
                _parse_transport_type(ns, r.find(ns + 'Line')),
                _parse_transport_name(ns, r.find(ns + 'Line')),
                _parse_deviations(ns, r.find(ns + 'Deviations')))

def _parse_journey(ns, j):
    rs = j.findall('%sRouteLinks/%sRouteLink' % (ns, ns))
    journey = Journey()
    for r in rs:
        link = _parse_route_link(ns, r)
        journey.addLink(link)
    return journey

def search_journey(start, stop, when):
    url = _build_url('resultspage.asp', { 'LastStart': when.strftime('%y-%m-%d %H:%M'),
                                          'cmdaction': 'next',
                                          'selPointFr': '%s|%d|0' % (start.getName().encode('utf-8'), start.getId()),
                                          'selPointTo': '%s|%d|0' % (stop.getName().encode('utf-8'), stop.getId()),
                                          })
    body = _send_req(url)
    open('/tmp/lastreq.xml', 'w').write(url)
    open('/tmp/lastrep.xml', 'w').write(body)
    tree = ElementTree()
    tree.parse(StringIO(body))
    root = tree.getroot()
    js = root.getiterator(NS_ETISWS + 'Journey')
    journeys = [ ]
    for j in js:
        journeys.append(_parse_journey(NS_ETISWS, j))
    return journeys

if __name__ == '__main__':
    a = search_station('lund c')[0]
    print a.getName(), a.getId()
    b = search_station('malm')[0]
    print b.getName(), b.getId()

    print '###########################################'
    js = search_journey(a, b, datetime.now())
    print 'Got %d hits' % len(js)
    for j in js:
        print 'Journey', j
        ls = j.getLinks()
        for l in ls:
            print l.getDepartureStation().getName(), l.getDepartureTime()

