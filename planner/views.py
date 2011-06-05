# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from api import search_station, search_journey
from datetime import datetime

class LinkView:
    def __init__(self, link):
        self._link = link
    def departure_name(self):
        return self._link.getDepartureStation().getName()
    def arrival_name(self):
        return self._link.getArrivalStation().getName()
    def pixel_length(self):
        return self._link.getDuration().seconds / 60 * 3
    def departure_time(self):
        return self._link.getDepartureTime().strftime("%H:%M")
    def arrival_time(self):
        return self._link.getArrivalTime().strftime("%H:%M")
    def transport_type(self):
        return self._link.getTransportType()
    def duration(self):
        return self._link.getDuration().seconds / 60
    def color(self):
        COLOR_MAP = {
            'Pågatåg': 'purple',
            'regionbuss': 'yellow',
            'Pendeln': 'yellow',
            'Skåneexpressen': 'yellow',
            'stadsbuss': 'green',
            'Öresundståg': 'gray',
            'färja': 'blue',
            }
        t = self._link.getTransportType()
        if COLOR_MAP.has_key(t):
            return COLOR_MAP[t]
        else:
            return "lightgray"

def transform_journey(j):
    links = j.getLinks()
    return map(lambda l: LinkView(l), links)

def transform_journeys(js):
    return map(transform_journey, js)
        
def start(req):
    return render_to_response('start.html')

def search(req):
    r_to = search_station(req.GET['to'].encode('iso-8859-1'))
    r_fr = search_station(req.GET['fr'].encode('iso-8859-1'))

    journeys = search_journey(r_fr[0], r_to[0], datetime.now())
    journeys = transform_journeys(journeys)

    info = { 
        'fr': r_fr[0].getName(),
        'to': r_to[0].getName(),
        'fr_alts': map(lambda x: x.getName(), r_fr[1:4]),
        'to_alts': map(lambda x: x.getName(), r_to[1:4]),
        'journeys': journeys,
        }
    return render_to_response('search.html', info)

def css(req):
    return render_to_response('planner.css')

def ajax_stations(req):
    stations = search_station(req.GET['term'].encode('iso-8859-1'))
    return render_to_response('ajax_stations.json', { 'stations': stations })
