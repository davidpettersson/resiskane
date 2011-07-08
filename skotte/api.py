# -*- encoding: utf-8 -*-
#
# api.py
#

from xml.etree.ElementTree import ElementTree
from StringIO import StringIO
from pprint import pprint
from domain import Journey, Link, Deviation
from models import Station
from datetime import datetime
from constants import NS, TRANSPORT_MAP
from network import send_req
from stations import lookup_station
from metaphone import dm

def search_station(qs):
    hits = [ ]
    try:
        hits.append(Station.objects.get(name__iexact=qs))
    except Station.DoesNotExist:
        pass

    mp = dm(qs)[0]
    for st in Station.objects.filter(metaphone__istartswith=mp):
        if not st in hits:
            hits.append(st)
    for st in Station.objects.filter(metaphone__icontains=mp):
        if not st in hits:
            hits.append(st)
    return hits

def _parse_date_time(ns, d):
    return datetime.strptime(d.text, '%Y-%m-%dT%H:%M:%S')

def _parse_station(ns, p):
    return lookup_station(int(p.find(ns + 'Id').text))

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

    body = send_req('resultspage.asp', { 'LastStart': when.strftime('%y-%m-%d %H:%M'),
                                         'cmdaction': 'next',
                                         'selPointFr': '%s|%d|0' % (start.name.encode('utf-8'), start.identifier),
                                         'selPointTo': '%s|%d|0' % (stop.name.encode('utf-8'), stop.identifier),
                                         })
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

