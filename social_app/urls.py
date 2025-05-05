from django.urls import path
from . import views

app_name = 'social_app'

urlpatterns = [
    # Main views
    path('', views.index, name='index'),
    path('reels/', views.reels_page, name='reels_page'),
    
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Posts
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    # Reels
    path('reel/create/', views.create_reel, name='create_reel'),
    path('reel/<int:reel_id>/', views.reel_detail, name='reel_detail'),
    path('reel/<int:reel_id>/like/', views.like_reel, name='like_reel'),
    path('reel/<int:reel_id>/delete/', views.delete_reel, name='delete_reel'),
    
    # User profiles
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),
    
    # Search
    path('search/', views.search, name='search'),
    
    # Friendship
    path('friends/', views.friends_list, name='friends_list'),
    path('friends/requests/', views.friendship_requests, name='friendship_requests'),
    path('friends/request/<str:username>/', views.send_friendship_request, name='send_friendship_request'),
    path('friends/accept/<int:request_id>/', views.accept_friendship_request, name='accept_friendship_request'),
    path('friends/reject/<int:request_id>/', views.reject_friendship_request, name='reject_friendship_request'),
    path('friends/cancel/<int:request_id>/', views.cancel_friendship_request, name='cancel_friendship_request'),
    path('friends/remove/<str:username>/', views.remove_friend, name='remove_friend'),
    
    # Messaging
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('messages/new/<str:username>/', views.new_conversation, name='new_conversation'),
    path('messages/ajax/send/', views.ajax_send_message, name='ajax_send_message'),
    path('messages/ajax/<int:conversation_id>/get/', views.ajax_get_messages, name='ajax_get_messages'),
]
