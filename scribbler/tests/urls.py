from django.conf.urls import include, url, handler404, handler500
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth import views as auth_views
from django.views.i18n import javascript_catalog


handler404 = 'scribbler.tests.urls.test_404'
handler500 = 'scribbler.tests.urls.test_500'


def test_404(request):
    return HttpResponseNotFound()


def test_500(request):
    return HttpResponseServerError()

js_info_dict = {
    'packages': ('scribbler', ),
}

urlpatterns = [
    url(r'^scribble/', include('scribbler.urls')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='jsi18n'),
    url(r'^test/', auth_views.login, {'template_name': 'test.html'}),
]
