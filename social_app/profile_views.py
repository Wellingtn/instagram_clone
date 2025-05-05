from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Profile, Follower, Post, Reel, Friendship, FriendshipRequest

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    reels = Reel.objects.filter(user=user).order_by('-created_at')
    
    # Check if the current user is following this user
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follower.objects.filter(follower=request.user, following=user).exists()
    
    # Check friendship status
    friendship_status = None
    if request.user.is_authenticated and request.user != user:
        # Check if they are friends
        if Friendship.objects.filter(user=request.user, friend=user).exists():
            friendship_status = 'friends'
        else:
            # Check for pending requests
            sent_request = FriendshipRequest.objects.filter(
                from_user=request.user, 
                to_user=user,
                status='pending'
            ).exists()
            
            received_request = FriendshipRequest.objects.filter(
                from_user=user, 
                to_user=request.user,
                status='pending'
            ).exists()
            
            if sent_request:
                friendship_status = 'request_sent'
            elif received_request:
                friendship_status = 'request_received'
            else:
                friendship_status = 'not_friends'
    
    # Get follower and following counts
    followers_count = Follower.objects.filter(following=user).count()
    following_count = Follower.objects.filter(follower=user).count()
    friends_count = Friendship.objects.filter(user=user).count()
    
    return render(request, 'social_app/profile/user_profile.html', {
        'profile_user': user,
        'posts': posts,
        'reels': reels,
        'is_following': is_following,
        'friendship_status': friendship_status,
        'followers_count': followers_count,
        'following_count': following_count,
        'friends_count': friends_count,
        'posts_count': posts.count(),
        'reels_count': reels.count()
    })

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    # Prevent following yourself
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
        return redirect('social_app:user_profile', username=username)
    
    # Check if already following
    follower_relation, created = Follower.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if created:
        messages.success(request, f"You are now following {username}.")
    else:
        # Unfollow if already following
        follower_relation.delete()
        messages.success(request, f"You have unfollowed {username}.")
    
    return redirect('social_app:user_profile', username=username)

@login_required
def edit_profile(request):
    # In a real app, you would have more profile fields to edit
    if request.method == 'POST':
        # Update user information
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        
        # Update or create profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('social_app:user_profile', username=request.user.username)
    
    # Get or create profile for the form
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    return render(request, 'social_app/profile/edit_profile.html', {
        'profile': profile
    })

def followers_list(request, username):
    user = get_object_or_404(User, username=username)
    followers = Follower.objects.filter(following=user).select_related('follower')
    
    return render(request, 'social_app/profile/followers_list.html', {
        'profile_user': user,
        'followers': followers
    })

def following_list(request, username):
    user = get_object_or_404(User, username=username)
    following = Follower.objects.filter(follower=user).select_related('following')
    
    return render(request, 'social_app/profile/following_list.html', {
        'profile_user': user,
        'following': following
    })
