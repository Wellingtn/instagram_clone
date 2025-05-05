from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FriendshipRequest(models.Model):
    """Model for friendship requests between users"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')
        
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"
    
    def accept(self):
        """Accept the friendship request and create a friendship"""
        self.status = 'accepted'
        self.save()
        
        # Create friendship (both ways to represent mutual connection)
        Friendship.objects.create(user=self.from_user, friend=self.to_user)
        Friendship.objects.create(user=self.to_user, friend=self.from_user)
        
        return True
    
    def reject(self):
        """Reject the friendship request"""
        self.status = 'rejected'
        self.save()
        return True


class Friendship(models.Model):
    """Model for friendships between users (mutual connection)"""
    user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'friend')
        
    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"
