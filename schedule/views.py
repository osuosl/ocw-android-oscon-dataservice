from datetime import date, timedelta
import json

from django.http import HttpResponse

from models import *


def session_day(request):
    """ filters session by days """
    timestamp = request.GET['t']
    date = date.fromtimestamp(timestamp)
    date_end = date + timedelta(1)
    list_ = [session.dict() for session in Event.objects.filter(start__gte=date, start__lte=date_end)]
    return HttpResponse(json.dumps(list_))

def sessions(request):
    list_ = [session.dict() for session in Event.objects.all()]
    return HttpResponse(json.dumps(list_))
    
    
def speakers(request):
    list_ = [o.dict() for o in Speaker.objects.all()]
    return HttpResponse(json.dumps(list_))


def tracks(request):
    list_ = [o.dict() for o in Track.objects.all()]
    return HttpResponse(json.dumps(list_))


def locations(request):
    list_ = [o.dict() for o in Location.objects.all()]
    return HttpResponse(json.dumps(list_))