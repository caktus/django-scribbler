from __future__ import unicode_literals

from django.http import HttpResponseNotFound, HttpResponseServerError
try:
    # Django 1.4+
    from django.conf.urls import include, patterns, url, handler404, handler500
except ImportError: # pragma: no cover
    # Django 1.3
    from django.conf.urls.defaults import include, patterns, url, handler404, handler500


handler404 = 'scribbler.tests.urls.test_404'
handler500 = 'scribbler.tests.urls.test_500'


def test_404(request):
    return HttpResponseNotFound()


def test_500(request):
    return HttpResponseServerError()


urlpatterns = patterns('',
    url(r'^scribble/', include('scribbler.urls')),
)
