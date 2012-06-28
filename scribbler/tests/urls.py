try:
    # Django 1.4+
    from django.conf.urls import include, patterns, url
except ImportError: # pragma: no cover
    # Django 1.3
    from django.conf.urls.defaults import include, patterns, url


urlpatterns = patterns('',
    url(r'^scribble/', include('scribbler.urls')),
)
