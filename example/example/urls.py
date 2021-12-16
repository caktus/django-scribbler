from django.urls import include, path

from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

from example.views import homepage
admin.autodiscover()


urlpatterns = [
    # Examples:
    # path(r'^$', 'example.views.home', name='home'),
    # path(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    path(r'admin/', admin.site.urls),
    path(r'scribble/', include('scribbler.urls')),
    path(r'jsi18n/', JavaScriptCatalog.as_view(packages=['scribbler']), name='jsi18n'),
    path(r'', homepage, name='home'),
]
