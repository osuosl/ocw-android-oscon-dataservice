from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    # Example:
    (r'^$', sessions),
    (r'sessions/$', sessions_day),
    (r'session/(\d+)$', session),
    (r'speaker/$', speaker),
    (r'tracks/$', tracks),
    (r'locations/$', locations),
)
