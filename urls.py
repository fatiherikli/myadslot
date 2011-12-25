from django.conf.urls.defaults import *
from django.template import add_to_builtins
from django.contrib import admin
from utils import here

add_to_builtins('myads.adserver.templatetags.datatags')
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


#serve static files
urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$',
     'serve', {
        #static directory root
        'document_root': here('static'),
        #directory listing
        'show_indexes': True }),)