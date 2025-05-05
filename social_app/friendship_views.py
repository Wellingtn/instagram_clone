from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q

from .models import FriendshipRequest, Friendship

@login_required
def friends_list(request):
    """View to display the user's friends"""
    friendships = Friendship.objects.filter(user=request.user).select_related('friend')
    
    context = {
        'friendships': friendships,
    }
    
    return render(request, 'social_app/friendship/friends_list.html', context)

@login_required
def friendship_requests(request):
    """View to display pending friendship requests"""
    received_requests = FriendshipRequest.objects.filter(
        to_user=request.user, 
        status='pending'
    ).select_related('from_user')
    
    sent_requests = FriendshipRequest.objects.filter(
        from_user=request.user,
        status='pending'
    ).select_related('to_user')
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    
    return render(request, 'social_app/friendship/friendship_requests.html', context)

@login_required
def send_friendship_request(request, username):
    """View to send a friendship request"""
    to_user = get_object_or_404(User, username=username)
    
    # Check if users are already friends
    if Friendship.objects.filter(user=request.user, friend=to_user).exists():
        messages.warning(request, f"You are already friends with {to_user.username}.")
        return redirect('social_app:user_profile', username=username)
    
    # Check if a request already exists
    existing_request = FriendshipRequest.objects.filter(
        from_user=request.user,
        to_user=to_user
    ).first()
    
    if existing_request:
        if existing_request.status == 'pending':
            messages.info(request, f"You already sent a friendship request to {to_user.username}.")
        elif existing_request.status == 'rejected':
            # If previously rejected, create a new request
            existing_request.status = 'pending'
            existing_request.save()
            messages.success(request, f"Friendship request sent to {to_user.username}.")
        return redirect('social_app:user_profile', username=username)
    
    # Check if there's a request from the other user
    reverse_request = FriendshipRequest.objects.filter(
        from_user=to_user,
        to_user=request.user,
        status='pending'
    ).first()
    
    if reverse_request:
        # Auto-accept the reverse request
        reverse_request.accept()
        messages.success(request, f"You are now friends with {to_user.username}!")
        return redirect('social_app:user_profile', username=username)
    
    # Create a new friendship request
    FriendshipRequest.objects.create(
        from_user=request.user,
        to_user=to_user
    )
    
    messages.success(request, f"Friendship request sent to {to_user.username}.")
    return redirect('social_app:user_profile', username=username)

@login_required
def accept_friendship_request(request, request_id):
    """View to accept a friendship request"""
    friendship_request = get_object_or_404(
        FriendshipRequest, 
        id=request_id, 
        to_user=request.user,
        status='pending'
    )
    
    friendship_request.accept()
    
    messages.success(request, f"You are now friends with {friendship_request.from_user.username}!")
    return redirect('social_app:friendship_requests')

@login_required
def reject_friendship_request(request, request_id):
    """View to reject a friendship request"""
    friendship_request = get_object_or_404(
        FriendshipRequest, 
        id=request_id, 
        to_user=request.user,
        status='pending'
    )
    
    friendship_request.reject()
    
    messages.info(request, f"You rejected the friendship request from {friendship_request.from_user.username}.")
    return redirect('social_app:friendship_requests')

@login_required
def cancel_friendship_request(request, request_id):
    """View to cancel a sent friendship request"""
    friendship_request = get_object_or_404(
        FriendshipRequest, 
        id=request_id, 
        from_user=request.user,
        status='pending'
    )
    
    friendship_request.delete()
    
    messages.info(request, f"Friendship request to {friendship_request.to_user.username} cancelled.")
    return redirect('social_app:friendship_requests')

@login_required
def remove_friend(request, username):
    """View to remove a friend"""
    friend = get_object_or_404(User, username=username)
    
    # Delete both friendship records (mutual connection)
    Friendship.objects.filter(
        Q(user=request.user, friend=friend) | 
        Q(user=friend, friend=request.user)
    ).delete()
    
    messages.info(request, f"{friend.username} has been removed from your friends.")
    return redirect('social_app:friends_list')
