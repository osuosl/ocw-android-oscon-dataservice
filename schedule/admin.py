from django.contrib import admin

from models import *


class EventInline(admin.TabularInline):
    model = Event
    fields= ('title','start','end')
    extra = 0   


class TrackAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    inlines = [EventInline]


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [EventInline]


class SpeakerInline(admin.StackedInline):
    model = Speaker
    extra = 0


class EventAdmin(admin.ModelAdmin):
    list_display = ('title','track','start', 'end')
    list_filter = ('track','location')
    search_fields = ('title','description')
    exclude=('speakers',)
    ordering = ('start',)


class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name','bio')
    inlines = [EventInline]


admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Speaker, SpeakerAdmin)