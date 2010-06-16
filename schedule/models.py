from datetime import datetime

from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=64, unique=True)
    color = models.CharField(max_length=6, default="AAAAAA")
    color_dark = models.CharField(max_length=6, default="888888")
    color_text = models.CharField(max_length=6, default="FFFFFF")

    def dict(self):
        return dict(
            name=self.name,
            color="#%s"%self.color,
            color_dark = "#%s"%self.color_dark,
            color_text = "#%s"%self.color_text
        )

    def __str__(self):
        return self.name

class Speaker(models.Model):
    oid = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=128)
    bio = models.TextField(max_length=4096, blank=True, null=True)
    affiliation = models.CharField(max_length=256, null=True, blank=True)
    website = models.CharField(max_length=256, null=True, blank=True)
    twitter = models.CharField(max_length=64, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    
    def dict(self):
        return dict(
            id = self.id,
            name = self.name,
            biography = self.bio,
            affiliation = self.affiliation,
            website = self.website,
            twitter = self.twitter
        )

    def __str__(self):
        return self.name


class Event(models.Model):
    oid = models.CharField(max_length=10, unique=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=4096)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, related_name="events")
    track = models.ForeignKey(Track, related_name="events", null=True)
    speakers = models.ManyToManyField(Speaker, related_name="events")
    display = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('start','end')
    
    def list_dict(self):
        """ returns just properties needed for event list """
        return dict(
            id = self.id,
            title = self.title,
            start_time = self.start.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
            end_time = self.end.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
            room_id = self.location_id,
            track_id = self.track_id,
            user_ids = [s.id for s in self.speakers.all()]
        )
        
    def detail_dict(self):
        """ returns all properties for the detail view """
        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            start_time = self.start.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
            end_time = self.end.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
            room_id = self.location_id,
            track_id = self.track_id,
            user_ids = [s.id for s in self.speakers.all()]
        )