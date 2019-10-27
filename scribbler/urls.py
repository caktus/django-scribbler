from django.conf.urls import url

from scribbler import views


urlpatterns = (
    url('^preview/(?P<ct_pk>(\d+))$', views.preview_scribble, name='preview-scribble'),
    url('^create/$', views.create_edit_scribble, name='create-scribble'),
    url('^edit/(?P<scribble_id>(\d+))/$', views.create_edit_scribble, name='edit-scribble'),
    url('^delete/(?P<scribble_id>(\d+))/$', views.delete_scribble, name='delete-scribble'),
    url('^edit-field/(?P<ct_pk>(\d+))/(?P<instance_pk>(\d+))/(?P<field_name>(\w+))/$',
        views.edit_scribble_field, name='edit-scribble-field'),
)
