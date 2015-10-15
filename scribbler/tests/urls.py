from django.conf.urls import include, url
from django.http import HttpResponseNotFound, HttpResponseServerError

from scribbler.tests.views import testpage

# try:
#     # Django 1.4+
#     from django.conf.urls import include, patterns, url, handler404, handler500
# except ImportError: # pragma: no cover
#     # Django 1.3
#     from django.conf.urls.defaults import include, patterns, url, handler404, handler500
#
#
# handler404 = 'scribbler.tests.urls.test_404'
# handler500 = 'scribbler.tests.urls.test_500'


def test_404(request):
    return HttpResponseNotFound()


def test_500(request):
    return HttpResponseServerError()

js_info_dict = {
    'packages': ('scribbler', ),
}

urlpatterns = [
    url(r'^scribble/', include('scribbler.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^test/', testpage, name='test'),
]
