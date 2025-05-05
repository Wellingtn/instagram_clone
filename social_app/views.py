# Main views file that imports and re-exports views from specialized modules
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Post, Reel, Follower

# Basic view for the index page
def index(request):
    """
    Main page view that shows recent posts and reels
    """
    posts = Post.objects.select_related('user').all().order_by('-created_at')[:10]
    reels = Reel.objects.select_related('user').all().order_by('-created_at')[:5]
    
    context = {
        'posts': posts,
        'reels': reels,
    }
    
    return render(request, 'social_app/index.html', context)

# Import views from specialized modules
from .auth_views import signup_view, login_view, logout_view
from .post_views import create_post, post_detail, like_post, delete_post
from .reel_views import create_reel, reel_detail, like_reel, delete_reel
from .profile_views import (
    user_profile, follow_user, edit_profile, 
    followers_list, following_list
)
from .search_views import search

# Re-export all views
__all__ = [
    'index',
    'signup_view', 'login_view', 'logout_view',
    'create_post', 'post_detail', 'like_post', 'delete_post',
    'create_reel', 'reel_detail', 'like_reel', 'delete_reel',
    'user_profile', 'follow_user', 'edit_profile', 'followers_list', 'following_list',
    'search',
]
