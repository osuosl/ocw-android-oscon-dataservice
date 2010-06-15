from datetime import date, timedelta
import json

from django.http import HttpResponse

from models import *


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