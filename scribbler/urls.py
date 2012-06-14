from django.conf.urls import patterns, url


urlpatterns = patterns('scribbler.views',
    url('^preview/$', 'preview_scribble', name='preview-scribble'),
)
