from django.urls import path
from .views import event_list, event_detail, create_event, edit_event, delete_event, create_location

urlpatterns = [
    path('events/', event_list, name='event_list'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('events/create/', create_event, name='create_event'),
    path('events/create-location/', create_location, name='create_location'),
    path('events/<int:event_id>/edit/', edit_event, name='edit_event'),
    path('events/<int:event_id>/delete/', delete_event, name='delete_event'),
]
