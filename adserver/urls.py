from django.conf.urls.defaults import *

urlpatterns = patterns('myads.adserver.views',
    url(r'^$', 'dashboard', name='dashboard'),

    # slot
    url(r'^slot/add', 'add_slot', name='adserver_add_slot'),
    url(r'^slot/(?P<slot>.*)/delete', 'delete_slot', name='adserver_delete_slot'),
    url(r'^slot/(?P<slot>.*)/edit', 'edit_slot', name='adserver_edit_slot'),
    url(r'^slot/(?P<slot>.*)/statistics', 'stats_slot', name='adserver_stats_slot'),
    url(r'^slot/(?P<slot>.*)/get_snippet$', 'get_slot_snippet', name='adserver_get_snippet'),
    url(r'^slot/(?P<slot>.*)/preview$', 'preview_slot', name='adserver_preview_slot'),
    url(r'^slot/(?P<slot>.*)/advertisements$', 'advertisements', name='adserver_ads'),



    # advertisements
    url(r'^advertisement/(?P<slot>.*)/add$', 'add_advertisement', name='adserver_add_advertisement'),
    url(r'^advertisement/(?P<ads_id>\d+)/delete$', 'delete_advertisement', name='adserver_delete_advertisement'),
    url(r'^advertisement/(?P<ads_id>\d+)/edit$', 'edit_advertisement', name='adserver_edit_advertisement'),
    url(r'^advertisement/(?P<ads_id>\d+)/visitors', 'advertisement_visitors', name='adserver_advertisement_visitors'),


    # tracking ads
    url(r'^(?P<username>.*)/(?P<slot>.*).js$', 'track', name='adserver_track_js'),
    url(r'^(?P<username>.*)/(?P<slot>.*)/information$', 'information_message', name='adserver_information_message'),

)

