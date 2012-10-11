from __future__ import unicode_literals

try:
    # Django 1.4+
    from django.conf.urls import patterns, url
except ImportError: # pragma: no cover
    # Django 1.3
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('scribbler.views',
    url('^preview/$', 'preview_scribble', name='preview-scribble'),
    url('^create/$', 'create_edit_scribble', name='create-scribble'),
    url('^edit/(?P<scribble_id>(\d+))/$', 'create_edit_scribble', name='edit-scribble'),
    url('^delete/(?P<scribble_id>(\d+))/$', 'delete_scribble', name='delete-scribble'),
)
