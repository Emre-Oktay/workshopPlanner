from django.contrib import admin

from .models import Event, Location, EventSessionItem, Tag, Category, Invitation, Comment

admin.site.register(Location)
admin.site.register(Event)
admin.site.register(EventSessionItem)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Invitation)
admin.site.register(Comment)
