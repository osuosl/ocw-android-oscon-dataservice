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

import httplib2
from datetime import datetime, timedelta


from django.db.models import Q
from BeautifulSoup import BeautifulSoup

from schedule.models import *


URI = 'http://www.oscon.com/oscon2010/public/schedule/full'

URIS = [
    ('http://www.oscon.com/oscon2010/public/schedule/stype/keynote','en_session en_plenary vevent'),
   #'http://www.oscon.com/oscon2010/public/schedule/stype/bof',
   ('http://www.oscon.com/oscon2010/public/schedule/stype/Event','en_session en_plenary vevent'),
   ('http://www.oscon.com/oscon2010/public/schedule/full','en_session vevent')
    ]


URI_SESSION = 'http://www.oscon.com/oscon2010/public/schedule/detail/%s'
URI_SPEAKER = 'http://www.oscon.com/oscon2010/public/schedule/speaker/%s'

LOCATIONS = {}
TRACKS = {}

EXPIRED = datetime.now() - timedelta(0, 500)

def load_data():
    """ loads data objects that are reused for many events """
    for location in Location.objects.all():
        LOCATIONS[location.name] = location
        LOCATIONS[location.display_name] = location
    for track in Track.objects.all():
        TRACKS[track.name] = track


def create_speaker_by_name(name):
    """ creates or finds a speaker by their name """
    try:
        speaker = Speaker.objects.get(name=name)
    except Speaker.DoesNotExist:
        speaker = Speaker()
        speaker.name=name
        speaker.save()
    return speaker


def parse_speaker(id):
    
    url = URI_SPEAKER % id
    http = httplib2.Http()
    response, html = http.request(url, 'GET')
    soup = BeautifulSoup(html)
    details = soup('div', attrs={'id':'mid'})[0]
    
    # name
    name_tag = details('h1', attrs={'class':'fn'})[0]
    name = scrub_html_strict(name_tag.contents[0].strip())
    print 'SPEAKER:', id, name
    
    try:
        speaker = Speaker.objects.get(Q(name=name)|Q(oid=id))
    except Speaker.DoesNotExist:
        speaker = Speaker()
        speaker.oid = id
    
    speaker.name = name
    
    # affiliation
    speaker.affiliation = name_tag('span', attrs={'class':'info'})[0].string
    
    # description
    bio_note = details('div', attrs={'class':'en_speaker_bio note'})[0]('p')
    if len(bio_note) >= 2:
        speaker.bio = bio_note[1].renderContents()
        
    # website
    link_tags = bio_note[0]('a')
    if len(link_tags) >= 1:
        speaker.website = link_tags[0]['href']
    
        # twitter
        if len(link_tags) == 2:
            twitter = link_tags[1].string
            speaker.twitter = None if twitter == 'Attendee Directory Profile' else twitter
    
    speaker.save()
    return speaker


def scrub_html(raw):
    #raw = raw.replace('&#8217;',"'")
    #raw = raw.replace('</span>','')
    #raw = raw.replace('<br>','\n')
    #raw = raw.replace('<br />','\n')
    #raw = raw.replace('<br/>','\n')
    #raw = raw.replace('<p>','')
    #raw = raw.replace('<b>','')
    #raw = raw.replace('</b>','')
    #raw = raw.replace('<strong>','')
    #raw = raw.replace('</strong>','')
    raw = raw.replace('<ul>','')
    raw = raw.replace('<ol>','')
    raw = raw.replace('</ul>','<br/>')
    raw = raw.replace('</ol>','<br/>')
    #raw = raw.replace('</p>','\n')
    raw = raw.replace('</li>','<br/>')
    #raw = raw.replace('&quot;','"')
    #raw = raw.replace('&amp;','&')
    raw = raw.replace('<li>','&nbsp;&nbsp;&nbsp;&#8226; ')
    #raw = raw.replace('&#38;','')
    #raw = raw.replace('&#8220','"')
    #raw = raw.replace('&#8221','"')
    #raw = raw.replace('&#8230','...')
    return raw


def scrub_html_strict(raw):
    raw = raw.replace('&#8217;',"'")
    raw = raw.replace('<b>','')
    raw = raw.replace('</b>','')
    raw = raw.replace('<strong>','')
    raw = raw.replace('</strong>','')
    raw = raw.replace('&quot;','"')
    raw = raw.replace('&amp;','&')    
    raw = raw.replace('&#38;','')
    raw = raw.replace('&#8220','"')
    raw = raw.replace('&#8221','"')
    raw = raw.replace('&#8230','...')
    raw = raw.replace('\n','')
    return raw


def parse_session(id, force=False):
    print 'parsing session: ', id
    url = URI_SESSION % id
    http = httplib2.Http()
    response, html = http.request(url, 'GET')
    soup = BeautifulSoup(html)
    details = soup('div', attrs={'id':'mid'})[0]
    
    try:
        event = Event.objects.get(oid=id)
        if event.updated > EXPIRED and not force:
            # record is not expired, skipping
            print 'skipping record'
            return
    except Event.DoesNotExist:
        event = Event()
        event.oid = id
    
    # title
    title = details('h1', attrs={'class':'summary'})[0].string.strip()
    event.title = scrub_html_strict(title)
    
    # Description
    description_tag = details('div', attrs={'class':'en_session_description description'})[0]
    raw = description_tag.renderContents()
    event.description = scrub_html(raw)
    
    #speaker(s)
    moderators = []
    speaker_tag = details('div', attrs={'class':'en_session_speakers'})[0]
    speaker_tag_a = speaker_tag('a')
    speakers = [str(t['href'])[35:] for t in speaker_tag_a]   
    if not speakers:
        # some sessions have a moderator instead of a speaker
        # mods don't have bios but we should create a speaker object
        # anyway
        mod = str(speaker_tag.string).strip()[14:].strip()
        moderators = [create_speaker_by_name(mod).id]
    
    # schedule
    # abbr dtstart/dtend
    try:
        event.start = datetime.strptime(details('abbr', 'dtstart dtstamp')[0]['title'], '%Y%m%dT%H%M')
        event.end = datetime.strptime(details('abbr', 'dtend')[0]['title'], '%Y%m%dT%H%M')
    except IndexError:
        # must have a start and end time
        return
    
    # Track(s)
    track_tags = details('span', attrs={'class':'en_session_topics category'})
    if track_tags:    
        track_name = track_tags[0]('a')[0].string.replace('&amp;','&')
    else:
        track_name = " "
    if track_name in TRACKS:
        event.track = TRACKS[track_name]
    else:
        track = Track()
        track.name = track_name
        track.save()
        TRACKS[track_name] = track
        event.track = track
    
    #location
    location_name = details('span', attrs={'class':'location'})[0].string
    if location_name in LOCATIONS:
        event.location = LOCATIONS[location_name]
    else:
        location = Location()
        location.name = location_name
        location.display_name = location_name
        location.save()
        LOCATIONS[location_name] = location
        
        event.location = location
    
    event.save()
    
    for id in speakers:
        speaker = parse_speaker(id)
        event.speakers.add(speaker)
    for mod in moderators:
        event.speakers.add(mod)

def parse_html(html, klass):
    load_data()
    try:
        soup = BeautifulSoup(html)
    except Exception, e:
        print 'EXCEPTION LOADING FILE (%s) : %s' % (file, e)
        return
    
    force = True
    
    session_tags = soup.findAll('div', attrs={'class':klass})
    for tag in session_tags[0:]:
    #    try:
            id_tag = tag('a', attrs={'class':"url uid"})
            if len(id_tag):
                id = id_tag[0]['name'][7:]
                parse_session(id, force)
            else:
                print 'no id >>>>', id_tag
    #    except Exception, e:
    #        print tag
    #        raise e
            #continue


def parse():
    for url, klass in URIS:
        http = httplib2.Http()
        response, html = http.request(url, 'GET')
        parse_html(html, klass)


if __name__ == '__main__':
    parse()

