from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name="register"), 
    path('login/', login_view, name="login"), 
    path('logout/', logout_view, name="logout"),
    path('home/', home_view, name="home"), 
    path('profile/', profile_view, name="profile"), 
    path('edit_description_profile/', edit_description_view, name="edit_description"), 
    path('search_profile/', search_profile_view, name="search_profile"), 
    path('profile/<int:profile_id>', show_profile_view, name="show_profile"),
    path('send_friend_request/<int:profile_id>', send_friend_request_view, name="send_friend_request"),
    path('cancel_friend_request/<int:profile_id>', cancel_friend_request_view, name="cancel_friend_request"), 
    path('add_friend/<int:friend_id>', add_friend_view, name="add_friend"), 
    path('decline_friend_request/<int:friend_id>', decline_friend_view, name="decline_friend_request"), 
    path('remove_friend/<int:friend_id>', remove_friend_view, name="remove_friend")
]
