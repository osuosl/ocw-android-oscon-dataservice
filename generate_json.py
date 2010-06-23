#!/usr/bin/env python

#!/usr/bin/env python
if __name__ == '__main__':
    import sys
    import os

    #python magic to add the current directory to the pythonpath
    sys.path.append(os.getcwd())

    # ==========================================================
    # Setup django environment 
    # ==========================================================
    if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    # ==========================================================
    # Done setting up django environment
    # ===================================================
from datetime import timedelta
import json
import time

from schedule.models import *
from schedule.views import conference_data, sessions_day_data


def write(name, data):
    f = open('./tmp/%s'%name, 'w')
    f.write(json.dumps(data))
    f.close()


def generate():
    conference = conference_data()
    write('conference.json', conference)
    
    #schedule objects
    first_date = Event.objects.all().order_by('start')[0].start
    end_date = Event.objects.all().order_by('-start')[0].start
    delta = end_date - first_date
    for i in range(delta.days):
        day = first_date+timedelta(i)
        data = sessions_day_data(day)
        timestamp = day.strftime('%Y_%m_%d')
        write('schedule_%s.json'%timestamp, data)
    
    #sessions
    for event in Event.objects.all():
        write('event_%s.json' % event.id, event.detail_dict())
    
    #speakers
    for speaker in Speaker.objects.all():
        write('speaker_%s.json' % speaker.id, speaker.dict())
    
    
    
    


if __name__ == '__main__':
    generate()

