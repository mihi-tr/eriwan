from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import funda.views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'funda.views.home', name='home'),
    # url(r'^eriwan/', include('eriwan.foo.urls')),
    url(r'^', include('funda.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
