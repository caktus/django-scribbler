from django.conf.urls import include, url

from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

from example.views import homepage
admin.autodiscover()


urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    url(r'^scribble/', include('scribbler.urls')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=['scribbler']), name='jsi18n'),
    url(r'^$', homepage, name='home'),
]
