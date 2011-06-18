from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('resiskane.planner.urls')),
)
