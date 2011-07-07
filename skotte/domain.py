class Journey(object):
    def __init__(self):
        self._links = [ ]
    def addLink(self, link):
        self._links.append(link)
    def getLinks(self):
        return self._links
    def getTotalDuration(self):
        return sum(map(lambda l: l.getDuration(), self._links))
    def __repr__(self):
        return u'Journey[links=%d]' % len(self._links)

class Deviation(object):
    def __init__(self, header, details):
        self._header = header
        self._details = details
    def getHeader(self):
        return self._header
    def getDetails(self):
        return self._details

class Link(object):
    def __init__(self, departure_time, departure_st, arrival_time, arrival_st, transport_type, transport_name, deviations):
        self._d_t = departure_time
        self._d_s = departure_st
        self._a_t = arrival_time
        self._a_s = arrival_st
        self._transport_type = transport_type
        self._transport_name = transport_name
        self._deviations = deviations
    def getArrivalTime(self):
        return self._a_t
    def getDepartureTime(self):
        return self._d_t
    def getArrivalStation(self):
        return self._a_s
    def getDepartureStation(self):
        return self._d_s
    def getTransportName(self):
        return self._transport_name
    def getTransportType(self):
        return self._transport_type
    def getDuration(self):
        return self._a_t - self._d_t
    def getDeviations(self):
        return self._deviations
    def __repr__(self):
        return u'%s -> %s' % (self._d_s, self._a_s)
