from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.i18n import javascript_catalog

from example.views import homepage
admin.autodiscover()

js_info_dict = {
    'packages': ('scribbler', ),
}

urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^scribble/', include('scribbler.urls')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='jsi18n'),
    url(r'^$', homepage, name='home'),
]
