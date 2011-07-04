from django.conf.urls.defaults import *

from views import start, resolve, search, css, robots, ajax_stations
import settings

urlpatterns = patterns('',
    # Example:
    (r'^$', start),
    (r'^resolve', resolve),
    (r'^search', search),
    (r'^css', css),
    (r'^robots.txt$', robots),
    (r'^ajax/stations', ajax_stations),
)

if settings.DEBUG:
    urlpatterns += patterns('', 
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    )
