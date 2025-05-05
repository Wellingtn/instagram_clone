from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    """Model for conversations between two users"""
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversation {self.id}"
    
    @property
    def last_message(self):
        """Get the last message in the conversation"""
        return self.messages.order_by('-created_at').first()
    
    @classmethod
    def get_or_create_conversation(cls, user1, user2):
        """Get or create a conversation between two users"""
        # Check if a conversation already exists
        conversations = Conversation.objects.filter(participants=user1).filter(participants=user2)
        
        if conversations.exists():
            return conversations.first()
        
        # Create a new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(user1, user2)
        return conversation


class Message(models.Model):
    """Model for messages within a conversation"""
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f"Message from {self.sender.username} in conversation {self.conversation.id}"
    
    def mark_as_read(self):
        """Mark the message as read"""
        self.is_read = True
        self.save()
