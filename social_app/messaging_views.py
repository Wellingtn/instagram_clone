from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q, Max, Count, F, OuterRef, Subquery

from .models import Conversation, Message, Friendship

@login_required
def inbox(request):
    """View to display the user's message inbox"""
    # Get all conversations for the current user with the latest message
    conversations = Conversation.objects.filter(
        participants=request.user
    ).annotate(
        latest_message_time=Max('messages__created_at'),
        unread_count=Count('messages', filter=Q(messages__is_read=False, messages__sender__id=F('participants__id')) & ~Q(messages__sender=request.user))
    ).order_by('-latest_message_time')
    
    # For each conversation, get the other participant
    for conversation in conversations:
        conversation.other_participant = conversation.participants.exclude(id=request.user.id).first()
    
    context = {
        'conversations': conversations,
    }
    
    return render(request, 'social_app/messaging/inbox.html', context)

@login_required
def conversation_detail(request, conversation_id):
    """View to display a conversation and send messages"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    other_participant = conversation.participants.exclude(id=request.user.id).first()
    
    # Mark unread messages as read
    Message.objects.filter(
        conversation=conversation,
        sender=other_participant,
        is_read=False
    ).update(is_read=True)
    
    # Get all messages in the conversation
    messages_list = conversation.messages.all()
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        
        if content:
            # Create a new message
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            # Update the conversation's updated_at timestamp
            conversation.save()
            
            return redirect('social_app:conversation_detail', conversation_id=conversation.id)
    
    context = {
        'conversation': conversation,
        'other_participant': other_participant,
        'messages': messages_list,
    }
    
    return render(request, 'social_app/messaging/conversation_detail.html', context)

@login_required
def new_conversation(request, username):
    """View to start a new conversation with a user"""
    other_user = get_object_or_404(User, username=username)
    
    # Check if users are friends (optional, remove if you want to allow messaging non-friends)
    if not Friendship.objects.filter(user=request.user, friend=other_user).exists():
        messages.error(request, f"You can only message users who are your friends.")
        return redirect('social_app:user_profile', username=username)
    
    # Get or create a conversation between the users
    conversation = Conversation.get_or_create_conversation(request.user, other_user)
    
    return redirect('social_app:conversation_detail', conversation_id=conversation.id)

@login_required
def ajax_send_message(request):
    """AJAX view to send a message"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        conversation_id = request.POST.get('conversation_id')
        content = request.POST.get('content', '').strip()
        
        if not conversation_id or not content:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
        
        try:
            conversation = Conversation.objects.get(id=conversation_id, participants=request.user)
            
            # Create a new message
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            
            # Update the conversation's updated_at timestamp
            conversation.save()
            
            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': message.id,
                    'content': message.content,
                    'created_at': message.created_at.strftime('%b %d, %Y, %I:%M %p'),
                    'is_sender': True
                }
            })
            
        except Conversation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Conversation not found'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def ajax_get_messages(request, conversation_id):
    """AJAX view to get new messages in a conversation"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            conversation = Conversation.objects.get(id=conversation_id, participants=request.user)
            last_message_id = request.GET.get('last_message_id')
            
            # Get messages newer than the last message ID
            if last_message_id:
                new_messages = conversation.messages.filter(id__gt=last_message_id)
            else:
                new_messages = conversation.messages.all()
            
            # Mark messages from the other user as read
            other_participant = conversation.participants.exclude(id=request.user.id).first()
            Message.objects.filter(
                conversation=conversation,
                sender=other_participant,
                is_read=False
            ).update(is_read=True)
            
            # Format messages for JSON response
            messages_data = []
            for message in new_messages:
                messages_data.append({
                    'id': message.id,
                    'content': message.content,
                    'created_at': message.created_at.strftime('%b %d, %Y, %I:%M %p'),
                    'is_sender': message.sender == request.user
                })
            
            return JsonResponse({
                'status': 'success',
                'messages': messages_data
            })
            
        except Conversation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Conversation not found'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
