from django.conf.urls.defaults import *

from views import start, search, css, ajax_stations

urlpatterns = patterns('',
    # Example:
    (r'^$', start),
    (r'^search', search),
    (r'^css', css),
    (r'^ajax/stations', ajax_stations),
)
