from datetime import date, timedelta
import json

from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from models import *


@cache_page(60 * 15)
def conference(request):
    """ basic conference info """
    return HttpResponse(json.dumps(conference_data()))


def conference_data():
    # get start/end date. first/last event in schedule
    first_date = Event.objects.all().order_by('start')[0].start
    end_date = Event.objects.all().order_by('-start')[0].start
    
    tracks = {}
    for track in Track.objects.all():
        tracks[track.id] = track.dict()
    
    locations = {}
    for location in Location.objects.all():
        locations[location.id] = dict(name=location.display_name)
    
    info = dict(
        start = first_date.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
        end = end_date.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
        tracks=tracks,
        locations=locations
    )
    return info


def sessions_day(request, timestamp):
    """ filters session by day """
    timestamp = float(timestamp)/1000
    day = date.fromtimestamp(timestamp)
    
    # use cache if available
    key = "sessions_%s" % day
    json_str = cache.get(key)
    if not json_str:
        # data wasn't cached
        data = sessions_day_data(day)
        json_str = json.dumps(data)
        cache.set(key, json_str, 60*15)
    return HttpResponse(json_str)


def sessions_day_data(day):
    date_end = day + timedelta(1)
    items = [session.list_dict() for session in Event.objects.filter(start__gte=day, start__lte=date_end)]
    return dict(items=items)


def sessions(request):
    """ lists all sessions """
    items = [session.list_dict() for session in Event.objects.all()]
    data = dict(items=items)
    return HttpResponse(json.dumps(data))


@cache_page(60 * 15)
def session(request, id):
    """ session details """
    session = Event.objects.get(id=id)
    json_ = json.dumps(session.detail_dict())
    return HttpResponse(json_)


@cache_page(60 * 15)
def speaker(request, id):
    """ speaker details """
    speaker = Speaker.objects.get(id=id)
    return HttpResponse(json.dumps(speaker.dict()))


def tracks(request):
    """ lists all tracks """
    list_ = [o.dict() for o in Track.objects.all()]
    return HttpResponse(json.dumps(list_))


def locations(request):
    """ lists all locations """
    list_ = [o.dict() for o in Location.objects.all()]
    return HttpResponse(json.dumps(list_))
