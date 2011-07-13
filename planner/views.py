# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from resiskane.skotte.api import search_station, search_journey
from datetime import datetime, timedelta
from skotte.models import Station
from fromeach import fromeach

class Segment(object):
    def is_wait(self):
        return False

class TweenView(Segment):
    def __init__(self, prev, next):
        self._prev = prev
        self._next = next
    def departure_name(self):
        return self._prev.getArrivalStation().name
    def arrival_name(self):
        return self._next.getDepartureStation().name
    def pixel_length(self):
        duration = self._next.getDepartureTime() - self._prev.getArrivalTime()
        return min(120, duration.seconds / 60) * 3 + 20
    def duration(self):
        duration = self._next.getDepartureTime() - self._prev.getArrivalTime()
        return duration.seconds / 60
    def departure_time(self):
        return self._prev.getArrivalTime().strftime("%H:%M")
    def arrival_time(self):
        return self._next.getDepartureTime().strftime("%H:%M")
    def transport_name(self):
        return 'vänta'
    def transport_short(self):
        return '&#x25f7;'
    def has_deviations(self):
        return False
    def deviations(self):
        return [ ]
    def transport(self, allow_short=False):
        return None
    def type_abbrev(self):
        return None
    def color(self):
        return 'white'
    def is_wait(self):
        return True

class LinkView(Segment):
    def __init__(self, link):
        self._link = link
    def departure_name(self):
        return self._link.getDepartureStation().name
    def arrival_name(self):
        return self._link.getArrivalStation().name
    def pixel_length(self):
        return min(120, self._link.getDuration().seconds / 60) * 3 + 20
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
    def has_deviations(self):
        return len(self._link.getDeviations()) > 0
    def deviations(self):
        return self._link.getDeviations()
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
            if allow_short and self.pixel_length() < 75:
                short = 'Ö-tåg'
            else:
                short = 'Öresundståg'
        elif type_ in [ 'regionbuss', 'Pendeln', 'stadsbuss' ]:
            if allow_short and self.pixel_length() < 45:
                short = name
            else:
                short = 'Buss %s' % name
        elif type_ in 'Skåneexpressen':
            if allow_short and self.pixel_length() < 95:
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

    # produce all transport segments
    views = map(lambda l: LinkView(l), links)

    # produce all inbetweens
    tweens = [ ]
    for k in range(len(links) - 1):
        prev, next = links[k], links[k+1]
        tweens.append(TweenView(prev, next))

    # merge them
    views = list(fromeach(views, tweens))

    # remove all zero inbetweens
    zerotweenp = lambda item: isinstance(item, LinkView) or item.duration() > 0
    len_before = len(views)
    views = filter(zerotweenp, views)
    len_after = len(views)

    # TODO: Remove, just for debug
    if len_before > len_after:
        print 'YAY'

    prefix = {
        'when': day_ref,
        'remains': time_left,
        }
    views.insert(0, prefix)

    return views

def transform_journeys(js):
    return map(transform_journey, js)

def start_anonymous(req):
    return render_to_response('start.html')

def start(req):
    fr_id = req.GET.get('fr_id', None)
    to_id = req.GET.get('to_id', None)

    if fr_id:
        fr = Station.objects.get(identifier=fr_id)
    else:
        fr = None

    if to_id:
        to = Station.objects.get(identifier=to_id)
    else:
        to = None

    start_state = {
        'fr': fr,
        'to': to,
    }

    return render_to_response('start.html', start_state)

def resolve(req):
    req_to = req.GET['to']
    req_fr = req.GET['fr']

    r_to = search_station(req_to)
    r_fr = search_station(req_fr)

    search_url = '/search?fr_id=%d&to_id=%d' % (r_fr[0].identifier, r_to[0].identifier)
    return redirect(search_url)

def top_five_stations(start_name):
    name = start_name[:]
    while name:
        stations = search_station(name)
        if stations and len(stations) > 4:
            break
        else:
            name = name[:-1]
    if stations and len(stations) > 4:
        return filter(lambda s: s.name != start_name, stations[0:5])
    else:
        return [ ]

def search(req):

    fr_id = int(req.GET['fr_id'])
    to_id = int(req.GET['to_id'])
                 
    journeys = search_journey(fr_id, to_id, datetime.now())
    journeys = transform_journeys(journeys)

    info = { 
        'fr': r_fr[0].getName(),
        'to': r_to[0].getName(),
        'fr_alts': map(lambda x: x.getName(), r_fr[1:6]),
        'to_alts': map(lambda x: x.getName(), r_to[1:6]),
        'journeys': journeys,
        }
    return render_to_response('search.html', info)

def robots(req):
    return render_to_response('robots.txt')

def station_list(req):
    stations = Station.objects.all().order_by('name')
    return render_to_response('station_list.html', { 'objects': stations })

def ajax_stations(req):
    req_term = req.GET['term']
    stations = search_station(req_term)[:10]
    return render_to_response('ajax_stations.json', { 'stations': stations })

