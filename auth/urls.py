from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^login/', 'myads.auth.views.login', name='auth_login'),
    url(r'^logout/', 'myads.auth.views.logout', name='auth_logout'),
    url(r'^register/', 'myads.auth.views.register', name='auth_register'),
    url(r'^complete/', 'myads.auth.views.complete', name='auth_complete'),

    # pricing urls
    url(r'^plans-and-pricing/', direct_to_template, {'template':'pricing.html'}, name='auth_pricing',),
)

