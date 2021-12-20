from django.urls import path, re_path

from scribbler import views


urlpatterns = (
    path('preview/<int:ct_pk>/', views.preview_scribble, name='preview-scribble'),
    path('create/', views.create_edit_scribble, name='create-scribble'),
    path('edit/<int:scribble_id>/', views.create_edit_scribble, name='edit-scribble'),
    path('delete/<int:scribble_id>/', views.delete_scribble, name='delete-scribble'),
    path('edit-field/<ct_pk>/<int:instance_pk>/<str:field_name>/',
        views.edit_scribble_field, name='edit-scribble-field'),
)
