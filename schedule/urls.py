from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    # Example:
    (r'^$', sessions),
    (r'speakers/$', speakers),
    (r'tracks/$', tracks),
    (r'locations/$', locations),
)
