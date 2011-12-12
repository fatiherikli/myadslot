from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/', 'myads.auth.views.login', name='auth_login'),
    url(r'^register/', 'myads.auth.views.register', name='auth_register'),
    url(r'^complete/', 'myads.auth.views.complete', name='auth_complete'),
)

