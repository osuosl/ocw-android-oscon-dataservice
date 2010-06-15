from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Track(models.Model):
    name = models.CharField(max_length=64, unique=True)
    color = models.CharField(max_length=6, default="AAAAAA")

    def dict(self):
        return dict(
            name=self.name,
            color=self.color
        )


class Speaker(models.Model):
    oid = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=128)
    bio = models.CharField(max_length=4096, blank=True, null=True)
    affiliation = models.CharField(max_length=256, null=True, blank=True)
    website = models.CharField(max_length=256, null=True, blank=True)
    twitter = models.CharField(max_length=64, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    
    def dict(self):
        return dict(
            id = self.id,
            name = self.name,
            bio = self.bio,
            affiliation = self.affiliation,
            website = self.website,
            twitter = self.twitter
        )


class Event(models.Model):
    oid = models.CharField(max_length=10, unique=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=4096)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, related_name="events")
    track = models.ForeignKey(Track, related_name="events", null=True)
    speakers = models.ManyToManyField(Speaker, related_name="events")
    
    def dict(self):
        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            #start = self.start,
            #end = self.end,
            location = self.location_id,
            track = self.track_id,
            speakers = [s.id for s in self.speakers.all()]
        )