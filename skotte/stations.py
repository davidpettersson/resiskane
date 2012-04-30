#
# stations.py -- station handling
#

from xml.etree.ElementTree import ElementTree
from StringIO import StringIO
from models import Station
from network import send_req
from constants import NS
from sys import stdout

def lookup_station(ident):
    return Station.objects.get(identifier=ident)

def populate_by_qs(s, output=stdout):
    encoded_s = s.encode('utf-8')
    output.write('QUERYING FOR %s\n' % encoded_s)
    body = send_req('querystation.asp', { 'inpPointFr': encoded_s })
    tree = ElementTree()
    tree.parse(StringIO(body))
    root = tree.getroot()
    points = root.getiterator(NS + 'Point')
    for point in points:
        station = Station()
        station.identifier = int(point.find(NS + 'Id').text)

        try:
            station = Station.objects.get(identifier=station.identifier)
        except Station.DoesNotExist:
            station.name = point.find(NS + 'Name').text
            station.x = int(point.find(NS + 'X').text)
            station.y = int(point.find(NS + 'Y').text)
            station.save()
            output.write('  STORED %s\n' % station.name.encode('utf-8'))
        except Station.MultipleObjectsReturned:
            output.write('  ERROR %d, %s\n' % (station.identifier, station.name.encode('utf-8')))
        else:
            # output.write('  IGNORE %s\n' % (station.name.encode('utf-8')))
            pass

