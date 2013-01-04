from django.conf.urls import patterns, include, url
import funda.views
# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'funda.views.home', name='home'),
    url(r'^questions/','funda.views.questions', name='questions'),
    url(r'^persons/','funda.views.persons', name='persons'),
    url(r'^keyword/(?P<id>\d+)','funda.views.keyword',name='keyword'),
    url(r'^person/(?P<parlid>\w+)','funda.views.person',name='person'),
    url(r'^asked/(?P<parlid>\w+)','funda.views.asked',name='person'),
    url(r'^question/(?P<parlid>\w+)','funda.views.question',name='question'),
    url(r'^term/(?P<term>\w+)','funda.views.term',name='term'),
    # url(r'^eriwan/', include('eriwan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
