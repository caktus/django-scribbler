try:
    # Django 1.4+
    from django.conf.urls import patterns, url
except ImportError: # pragma: no cover
    # Django 1.3
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('scribbler.views',
    url('^preview/(?P<slug>(\w|-)+)/$', 'preview_scribble', name='preview-scribble'),
)
