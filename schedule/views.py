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
        tracks[track.id] = dict(name=track.name, color=track.color, color_dark=256)
    
    info = dict(
        start = first_date.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
        end = end_date.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
        tracks=tracks,
    )
    
    return HttpResponse(json.dumps(info))

def sessions_day(request):
    """ filters session by day """
    timestamp = float(request.GET['t'])
    day = date.fromtimestamp(timestamp)
    date_end = day + timedelta(1)
    list_ = [session.list_dict() for session in Event.objects.filter(start__gte=day, start__lte=date_end)]
    return HttpResponse(json.dumps(list_))


def sessions(request):
    """ lists all sessions """
    list_ = [session.list_dict() for session in Event.objects.all()]
    return HttpResponse(json.dumps(list_))


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