# -*- encoding: utf-8 -*-

from urllib2 import urlopen
from urllib import urlencode
from xml.etree.ElementTree import ElementTree
from StringIO import StringIO
from pprint import pprint
from domain import Journey, Link, Deviation
from models import Station
from datetime import datetime
from metaphone import dm

NS = '{http://www.etis.fskab.se/v1.0/ETISws}'

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

def _refresh_by_search_key(s):
    encoded_s = s.encode('utf-8')
    url = _build_url('querystation.asp', { 'inpPointFr': encoded_s })
    body = _send_req(url)
    tree = ElementTree()
    tree.parse(StringIO(body))
    root = tree.getroot()
    points = root.getiterator(NS + 'Point')
    for point in points:
        station = Station()
        station.identifier = int(point.find(NS + 'Id').text)

        try:
            Station.objects.get(identifier=station.identifier)
        except Station.DoesNotExist:
            station.name = point.find(NS + 'Name').text
            station.x = int(point.find(NS + 'X').text)
            station.y = int(point.find(NS + 'Y').text)
            station.metaphone = dm(point.find(NS + 'Name').text)[0]
            station.save()
            print 'Saved', station.identifier
        except Station.MultipleObjectsReturned:
            print 'Cannot happen, multiple instances of', station.identifier
        else:
            print 'Already have', station.identifier

def search_station(qs):
    _refresh_by_search_key(qs)
    hits = [ ]
    try:
        hits.append(Station.objects.get(name__iexact=qs))
    except Station.DoesNotExist:
        pass

    mp = dm(qs)[0]
    hits.extend(Station.objects.filter(metaphone__icontains=mp))
    return hits

def _parse_date_time(ns, d):
    return datetime.strptime(d.text, '%Y-%m-%dT%H:%M:%S')

def _parse_station(ns, p):
    # TODO: This is really ugly
    _refresh_by_search_key(p.find(ns + 'Name').text)
    return Station.objects.get(identifier=int(p.find(ns + 'Id').text))

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

def search_journey(fr_id, to_id, when):
    start = Station.objects.get(identifier=fr_id)
    stop = Station.objects.get(identifier=to_id)

    url = _build_url('resultspage.asp', { 'LastStart': when.strftime('%y-%m-%d %H:%M'),
                                          'cmdaction': 'next',
                                          'selPointFr': '%s|%d|0' % (start.name.encode('utf-8'), start.identifier),
                                          'selPointTo': '%s|%d|0' % (stop.name.encode('utf-8'), stop.identifier),
                                          })
    body = _send_req(url)
    open('/tmp/lastreq.xml', 'w').write(url)
    open('/tmp/lastrep.xml', 'w').write(body)
    tree = ElementTree()
    tree.parse(StringIO(body))
    root = tree.getroot()
    js = root.getiterator(NS + 'Journey')
    journeys = [ ]
    for j in js:
        journeys.append(_parse_journey(NS, j))
    return journeys

if __name__ == '__main__':
    a = search_station('lund c')[0]
    print a.name, a.identifier
    b = search_station('malm')[0]
    print b.name, b.identifier

    print '###########################################'
    js = search_journey(a, b, datetime.now())
    print 'Got %d hits' % len(js)
    for j in js:
        print 'Journey', j
        ls = j.getLinks()
        for l in ls:
            print l.getDepartureStation().name, l.getDepartureTime()

