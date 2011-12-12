from django.conf.urls.defaults import *

urlpatterns = patterns('myads.adserver.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^add-slot', 'add_slot', name='adserver_add_slot'),
    url(r'^(?P<slot>.*)/$', 'advertisements', name='adserver_ads'),
    url(r'^(?P<slot>.*)/add$', 'add_advertisement', name='adserver_add_advertisement'),
    url(r'^(?P<slot>.*)/(?P<ads_id>\d+)/edit$', 'edit_advertisement', name='adserver_edit_advertisement'),
    url(r'^(?P<slot>.*)/get_snippet$', 'get_slot_snippet', name='adserver_get_snippet'),
    url(r'^(?P<slot>.*)/preview$', 'preview_slot', name='adserver_preview_slot'),

    # tracking ads
    url(r'^(?P<username>.*)/(?P<slot>.*).js$', 'track', name='adserver_track_js'),

)

