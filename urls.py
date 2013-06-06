from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ipdb.views.home', name='home'),
    # url(r'^ipdb/', include('ipdb.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^ip/',   'ipdb_mptt.ip.views.index', name='index'),
    url(r'^ip/',   include('ipdb.ip.urls')),

    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
