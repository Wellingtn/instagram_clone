from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Exists, OuterRef
import random

from .models import Post, Reel, Friendship

@login_required
def friends_feed(request):
    """View to display posts from the user's friends"""
    # Get IDs of the user's friends
    friend_ids = Friendship.objects.filter(user=request.user).values_list('friend_id', flat=True)
    
    # Get posts from friends, ordered by creation date
    posts = Post.objects.filter(
        user_id__in=friend_ids
    ).select_related('user').order_by('-created_at')
    
    # Add a flag to indicate if the current user has liked each post
    for post in posts:
        post.user_has_liked = post.likes.filter(user=request.user).exists()
    
    context = {
        'posts': posts,
        'page_title': 'Friends Feed'
    }
    
    return render(request, 'social_app/feed/friends_feed.html', context)

@login_required
def explore_reels(request):
    """View to display random reels for exploration"""
    # Get a sample of reels, ordered by popularity (likes count)
    # Exclude reels from the current user if desired
    reels = Reel.objects.exclude(user=request.user).annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count', '-created_at')[:50]  # Limit to 50 for performance
    
    # Convert to list and shuffle for randomness
    reels_list = list(reels)
    random.shuffle(reels_list)
    
    # Limit to a reasonable number to display
    reels_list = reels_list[:15]
    
    # Add a flag to indicate if the current user has liked each reel
    for reel in reels_list:
        reel.user_has_liked = reel.likes.filter(user=request.user).exists()
    
    context = {
        'reels': reels_list,
        'page_title': 'Explore Reels'
    }
    
    return render(request, 'social_app/feed/explore_reels.html', context)
