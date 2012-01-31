from django.contrib import admin
from adserver.models import AdSlot, Advertisement, Visitor, Message


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'user','view_count', )


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'advertisement', 'visit_count', 'last_visit_url', 'last_visit_date')

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Message)
admin.site.register(AdSlot)

