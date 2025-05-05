# Main views file that imports and re-exports views from specialized modules
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Post, Reel, Follower, Friendship

# Basic view for the index page (now shows friends' posts)
@login_required
def index(request):
    """
    Main page view that shows posts from friends (feed)
    """
    # Get IDs of the user's friends
    friend_ids = Friendship.objects.filter(user=request.user).values_list('friend_id', flat=True)
    
    # Get posts from friends, ordered by creation date
    posts = Post.objects.filter(
        user_id__in=friend_ids
    ).select_related('user').order_by('-created_at')
    
    # If no friends yet, show some recent posts as suggestions
    if not posts:
        posts = Post.objects.select_related('user').all().order_by('-created_at')[:5]
    
    # Add a flag to indicate if the current user has liked each post
    for post in posts:
        post.user_has_liked = post.likes.filter(user=request.user).exists()
    
    context = {
        'posts': posts,
        'page_title': 'Feed'
    }
    
    return render(request, 'social_app/index.html', context)

# View for reels page
@login_required
def reels_page(request):
    """
    View that shows random reels for exploration
    """
    # Get reels, ordered by popularity (likes count)
    reels = Reel.objects.annotate(
        likes_count=Count('likes')
    ).order_by('-created_at')[:20]  # Get recent reels
    
    # Add a flag to indicate if the current user has liked each reel
    for reel in reels:
        reel.user_has_liked = reel.likes.filter(user=request.user).exists()
    
    context = {
        'reels': reels,
        'page_title': 'Reels'
    }
    
    return render(request, 'social_app/reels_page.html', context)

# Import views from specialized modules
from .auth_views import signup_view, login_view, logout_view
from .post_views import create_post, post_detail, like_post, delete_post
from .reel_views import create_reel, reel_detail, like_reel, delete_reel
from .profile_views import (
    user_profile, follow_user, edit_profile, 
    followers_list, following_list
)
from .search_views import search
from .friendship_views import (
    friends_list, friendship_requests, send_friendship_request,
    accept_friendship_request, reject_friendship_request,
    cancel_friendship_request, remove_friend
)
from .messaging_views import (
    inbox, conversation_detail, new_conversation,
    ajax_send_message, ajax_get_messages
)

# Re-export all views
__all__ = [
    'index', 'reels_page',
    'signup_view', 'login_view', 'logout_view',
    'create_post', 'post_detail', 'like_post', 'delete_post',
    'create_reel', 'reel_detail', 'like_reel', 'delete_reel',
    'user_profile', 'follow_user', 'edit_profile', 'followers_list', 'following_list',
    'search',
    'friends_list', 'friendship_requests', 'send_friendship_request',
    'accept_friendship_request', 'reject_friendship_request',
    'cancel_friendship_request', 'remove_friend',
    'inbox', 'conversation_detail', 'new_conversation',
    'ajax_send_message', 'ajax_get_messages',
]
