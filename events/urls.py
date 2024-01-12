from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/',
         views.delete_event, name='delete_event'),

    path('events/create-location/', views.create_location, name='create_location'),

    path('events/<int:event_id>/create-session-item/',
         views.create_session_item, name='create_session_item'),
    path('events/<int:event_id>/edit-session/<int:session_id>/',
         views.edit_session_item, name='edit_session_item'),

    path('comment/<int:comment_id>/delete/',
         views.delete_comment, name='delete_comment'),

    path('events/<int:event_id>/register/',
         views.register_to_event, name='register_to_event'),

    path('events/<int:event_id>/bookmark/',
         views.bookmark_event, name='bookmark_event'),
    path('bookmarks/', views.bookmarked_events, name='bookmarked_events'),
]
