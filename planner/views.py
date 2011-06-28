# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from api import search_station, search_journey
from datetime import datetime, timedelta

class LinkView:
    def __init__(self, link):
        self._link = link
    def departure_name(self):
        return self._link.getDepartureStation().getName()
    def arrival_name(self):
        return self._link.getArrivalStation().getName()
    def pixel_length(self):
        return min(120, self._link.getDuration().seconds / 60) * 5 + 20
    def departure_time(self):
        return self._link.getDepartureTime().strftime("%H:%M")
    def arrival_time(self):
        return self._link.getArrivalTime().strftime("%H:%M")
    def transport_name(self):
        return self._link.getTransportName()
    def transport_type(self):
        return self._link.getTransportType()
    def duration(self):
        return self._link.getDuration().seconds / 60
    def transport_short(self):
        return self.transport(True)
    def transport(self, allow_short=False):
        name = self._link.getTransportName()
        type_ = self._link.getTransportType()
        short = ' '
        if type_ in 'Pågatåg':
            if allow_short and self.pixel_length() < 40:
                short = 'P-tåg'
            else:
                short = 'Pågatåg'
        elif type_ in 'Öresundståg':
            if allow_short and self.pixel_length() < 70:
                short = 'Ö-tåg'
            else:
                short = 'Öresundståg'
        elif type_ in [ 'regionbuss', 'Pendeln', 'stadsbuss' ]:
            if allow_short and self.pixel_length() < 45:
                short = name
            else:
                short = 'Buss %s' % name
        elif type_ in 'Skåneexpressen':
            if allow_short and self.pixel_length() < 90:
                short = 'SkE %s' % name.split()[1]
            else:
                short = u'SkåneExpressen %s' % name.split()[1]
        elif type_ in 'färja':
            short = name
        elif type_ in 'gång':
            short = 'Gång'
        return short
    def type_abbrev(self):
        TYPE_MAP = {
            'Pågatåg': 'tåg',
            'regionbuss': 'buss',
            'Pendeln': 'buss',
            'Skåneexpressen': 'buss',
            'stadsbuss': 'buss',
            'Öresundståg': 'tåg',
            'färja': 'färja',
            'gång': 'gång',
            'bil': 'bil',
            }
        t = self._link.getTransportType()
        if TYPE_MAP.has_key(t):
            return TYPE_MAP[t]
        else:
            return ' '
        
    def color(self):
        COLOR_MAP = {
            'Pågatåg': 'purple',
            'regionbuss': 'yellow',
            'Pendeln': 'yellow',
            'Skåneexpressen': 'yellow',
            'stadsbuss': 'green',
            'Öresundståg': 'gray',
            'färja': 'blue',
            'bil': 'black',
            }
        t = self._link.getTransportType()
        if COLOR_MAP.has_key(t):
            return COLOR_MAP[t]
        else:
            return "lightgray"

def transform_journey(j):
    links = j.getLinks()
    now = datetime.now()
    departure = links[0].getDepartureTime()
    one_day = timedelta(days=1)
    if departure.day == now.day:
        day_ref = departure.strftime('idag %H:%M')
    elif departure.day == (now + one_day).day:
        day_ref = departure.strftime('imorgon %H:%M')
    elif departure.day == (now + one_day + one_day).day:
        day_ref = departure.strftime('i övermorgon %H:%M')
    else:
        day_ref = departure.strftime('%Y-%m-%d, %H:%M')
    delta = departure - now
    remainder = int(delta.days * 24 * 60 + delta.seconds / 60)
    if remainder < 3:
        time_left = 'just nu'
    elif remainder < 13:
        time_left = 'om några minuter'
    elif remainder < 16:
        time_left = 'om en kvart'
    elif remainder < 35:
        time_left = 'inom en halvtimme'
    elif remainder == 45:
        time_left = 'om trekvart'
    elif remainder < 60:
        time_left = 'inom en timme'
    elif remainder < 120:
        time_left = 'inom två timmar'
    elif remainder < 180:
        time_left = 'inom tre timmar'
    else:
        time_left = 'om %d timmar' % (remainder / 60)
    
    prefix = {
        'when': day_ref,
        'remains': time_left,
        }
    views = map(lambda l: LinkView(l), links)
    views.insert(0, prefix)
    return views

def transform_journeys(js):
    return map(transform_journey, js)
        
def start(req):
    n_to = req.GET.get('to', '')
    n_fr = req.GET.get('fr', '')
    start_state = {
        'fr': n_fr,
        'to': n_to
    }
    return render_to_response('start.html', start_state)

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

def robots(req):
    return render_to_response('robots.txt')

def ajax_stations(req):
    stations = search_station(req.GET['term'].encode('iso-8859-1'))
    return render_to_response('ajax_stations.json', { 'stations': stations })
