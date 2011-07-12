from django.conf.urls.defaults import *
from settings import DEBUG, STATIC_DOC_ROOT
from views import *

urlpatterns = patterns('',
    # Example:
    (r'^$', start_anonymous),
    (r'^start', start),
    (r'^resolve', resolve),
    (r'^search', search),
    (r'^robots.txt$', robots),
    (r'^stations', station_list),
    (r'^ajax/stations', ajax_stations),
)

if DEBUG:
    urlpatterns += patterns('', 
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': STATIC_DOC_ROOT}),
    )
