from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    # Example:
        
    (r'^$', sessions),
    
    (r'conference/$', conference),
    
    (r'session/$', sessions),
    (r'sessions_day/(\d+)$', sessions_day),
    
    (r'session/(\d+)$', session),
    (r'speaker/(\d+)$', speaker),
    (r'tracks/$', tracks),
    (r'locations/$', locations),
)
