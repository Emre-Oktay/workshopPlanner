from django.urls import path
from .views import register_view, login_view, logout_view, user_view, update_user_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/<int:user_id>/', user_view, name='user'),
    path('update-user/', update_user_view, name='update-user'),
]
