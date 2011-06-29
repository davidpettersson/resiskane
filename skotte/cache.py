from redis import Redis
from time import time
from hashlib import sha1
from domain import Station

_REDIS_PORT = 17666
# _VALID_FOR = 60 * 60 * 24
_VALID_FOR = 20

def _hash_key(key):
    s = sha1()
    s.update(key)
    return s.hexdigest().lower()

def _write_station(r, st):
    prefix = 'station:%d:' % st.getId()
    r.set(prefix + 'name', st.getName())

def set_station_cache(key, stations):
    cache_key = 'station:cache:%s' % _hash_key(key)
    print 'INSERT', cache_key, key
    created_key = 'station:cache:%s:created' % _hash_key(key)
    r = Redis(port=_REDIS_PORT)
    for k, station in enumerate(stations):
        _write_station(r, station)
        r.zadd(cache_key, station.getId(), k)
    r.set(created_key, int(time()))

def _delete_station(r, stid):
    prefix = 'station:%d:' % stid
    r.delete(prefix + 'created')
    r.delete(prefix + 'name')

def _read_station(r, stid):
    now = int(time())
    prefix = 'station:%d:' % stid
    name = r.get(prefix + 'name')
    return Station(stid, name)

def get_station_cache(key):
    r = Redis(port=_REDIS_PORT)
    cache_key = 'station:cache:%s' % _hash_key(key)
    created_key = 'station:cache:%s:created' % _hash_key(key)
    # check if exists
    if not r.exists(cache_key):
        print 'MISS', cache_key, key
        return [ ]
    # check if valid
    created = r.get(created_key)
    if created + _VALID_FOR < int(time()):
        print 'EXPIRED', cache_key, key
        r.delete(created_key)
        r.delete(cache_key)
        return [ ]
    # load members
    members = r.zrange(cache_key, 0, -1)
    print 'HIT', members, key
    stations = [ ]
    for member in members:
        stations.append(_read_station(r, member))
    return stations
