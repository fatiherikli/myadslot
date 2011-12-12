from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # main urls
    url(r'^$', 'myads.core.views.index', name='index'),

    # auth urls
    (r'^auth/', include('myads.auth.urls')),

    # adserver urls
    (r'^adserver/', include('myads.adserver.urls')),

    # admin urls
    (r'^admin/', include(admin.site.urls)),
)
