from datetime import date, timedelta
import json

from django.http import HttpResponse

from models import *


def conference(request):
    """ basic conference info """
    
    # get start/end date. first/last event in schedule
    first_date = Event.objects.all().order_by('start')[0].start
    end_date = Event.objects.all().order_by('-start')[0].start
    
    tracks = {}
    for track in Track.objects.all():
        tracks[track.id] = dict(name=track.name, color=-5592406, color_dark=-5592406)
    
    locations = {}
    for location in Location.objects.all():
        locations[location.id] = dict(name=location.name)
    
    info = dict(
        start = first_date.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
        end = end_date.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
        tracks=tracks,
        locations=locations
    )
    
    return HttpResponse(json.dumps(info))

def sessions_day(request):
    """ filters session by day """
    timestamp = float(request.GET['t'])
    day = date.fromtimestamp(timestamp)
    date_end = day + timedelta(1)
    items = [session.list_dict() for session in Event.objects.filter(start__gte=day, start__lte=date_end)]
    data = dict(items=items)
    return HttpResponse(json.dumps(data))


def sessions(request):
    """ lists all sessions """
    items = [session.list_dict() for session in Event.objects.all()]
    data = dict(items=items)
    return HttpResponse(json.dumps(data))


def session(request, id):
    """ session details """
    session = Event.objects.get(id=id)
    return HttpResponse(json.dumps(session.detail_dict()))


def speaker(request):
    """ speaker details """
    list_ = [o.dict() for o in Speaker.objects.all()]
    return HttpResponse(json.dumps(list_))


def tracks(request):
    """ lists all tracks """
    list_ = [o.dict() for o in Track.objects.all()]
    return HttpResponse(json.dumps(list_))


def locations(request):
    """ lists all locations """
    list_ = [o.dict() for o in Location.objects.all()]
    return HttpResponse(json.dumps(list_))