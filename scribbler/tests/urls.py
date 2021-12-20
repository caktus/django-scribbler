from django.conf.urls import include, handler404, handler500
from django.urls import re_path
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth import views as auth_views
from django.views.i18n import JavaScriptCatalog


javascript_catalog = JavaScriptCatalog.as_view()


def test_404(request, exception=None):
    return HttpResponseNotFound()


def test_500(request, exception=None):
    return HttpResponseServerError()


js_info_dict = {
    'packages': ('scribbler', ),
}

login_url = re_path(r'^test/', auth_views.LoginView.as_view(template_name='test.html'))

urlpatterns = [
    re_path(r'^scribble/', include('scribbler.urls')),
    re_path(r'^jsi18n/$', javascript_catalog, js_info_dict, name='jsi18n'),
    login_url,
]
