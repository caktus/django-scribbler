from django.conf.urls import patterns, url


urlpatterns = patterns('scribbler.views',
    url('^preview/(?P<slug>(\w|-)+)/$', 'preview_scribble', name='preview-scribble'),
)
