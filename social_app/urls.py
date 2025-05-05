from django.urls import path
from . import views
from . import auth_views, post_views, reel_views, profile_views, search_views
from . import friendship_views, messaging_views

app_name = 'social_app'

urlpatterns = [
    # Main views
    path('', views.index, name='index'),
    
    # Authentication
    path('signup/', auth_views.signup_view, name='signup'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Posts
    path('post/create/', post_views.create_post, name='create_post'),
    path('post/<int:post_id>/', post_views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', post_views.like_post, name='like_post'),
    path('post/<int:post_id>/delete/', post_views.delete_post, name='delete_post'),
    
    # Reels
    path('reel/create/', reel_views.create_reel, name='create_reel'),
    path('reel/<int:reel_id>/', reel_views.reel_detail, name='reel_detail'),
    path('reel/<int:reel_id>/like/', reel_views.like_reel, name='like_reel'),
    path('reel/<int:reel_id>/delete/', reel_views.delete_reel, name='delete_reel'),
    
    # User profiles
    path('profile/<str:username>/', profile_views.user_profile, name='user_profile'),
    path('profile/<str:username>/follow/', profile_views.follow_user, name='follow_user'),
    path('profile/edit/', profile_views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/followers/', profile_views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', profile_views.following_list, name='following_list'),
    
    # Search
    path('search/', search_views.search, name='search'),
    
    # Friendship
    path('friends/', friendship_views.friends_list, name='friends_list'),
    path('friends/requests/', friendship_views.friendship_requests, name='friendship_requests'),
    path('friends/request/<str:username>/', friendship_views.send_friendship_request, name='send_friendship_request'),
    path('friends/accept/<int:request_id>/', friendship_views.accept_friendship_request, name='accept_friendship_request'),
    path('friends/reject/<int:request_id>/', friendship_views.reject_friendship_request, name='reject_friendship_request'),
    path('friends/cancel/<int:request_id>/', friendship_views.cancel_friendship_request, name='cancel_friendship_request'),
    path('friends/remove/<str:username>/', friendship_views.remove_friend, name='remove_friend'),
    
    # Messaging
    path('messages/', messaging_views.inbox, name='inbox'),
    path('messages/<int:conversation_id>/', messaging_views.conversation_detail, name='conversation_detail'),
    path('messages/new/<str:username>/', messaging_views.new_conversation, name='new_conversation'),
    path('messages/ajax/send/', messaging_views.ajax_send_message, name='ajax_send_message'),
    path('messages/ajax/<int:conversation_id>/get/', messaging_views.ajax_get_messages, name='ajax_get_messages'),
]
