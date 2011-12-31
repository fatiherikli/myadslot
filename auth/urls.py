from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^login/', 'myads.auth.views.login', name='auth_login'),
    url(r'^logout/', 'myads.auth.views.logout', name='auth_logout'),
    url(r'^register/', 'myads.auth.views.register', name='auth_register'),
    url(r'^complete/', 'myads.auth.views.complete', name='auth_complete'),
    url(r'^change-password/', 'myads.auth.views.change_password', name='auth_change_password'),
    url(r'^my-profile/', 'myads.auth.views.update_profile', name='auth_update_profile'),
    url(r'^inbox/$', 'myads.auth.views.inbox', name='auth_inbox'),
    url(r'^inbox/read/(?P<message_id>\d+)', 'myads.auth.views.read', name='auth_inbox_read'),
    url(r'^inbox/action/(?P<action>.*)/(?P<message_id>\d+)', 'myads.auth.views.inbox_action', name='auth_inbox_action'),

    # pricing urls
    url(r'^plans-and-pricing/', direct_to_template, {'template':'pricing.html'}, name='auth_pricing',),
)

