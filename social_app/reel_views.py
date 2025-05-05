from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Reel, ReelLike, ReelComment
from .forms import ReelForm, ReelCommentForm

@login_required
def create_reel(request):
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            reel = form.save(commit=False)
            reel.user = request.user
            reel.save()
            messages.success(request, 'Reel created successfully!')
            return redirect('social_app:index')
    else:
        form = ReelForm()
    return render(request, 'social_app/reel/create_reel.html', {'form': form})

def reel_detail(request, reel_id):
    reel = get_object_or_404(Reel, id=reel_id)
    comments = reel.comments.all().order_by('-created_at')
    
    # Check if the current user has liked the reel
    user_liked = False
    if request.user.is_authenticated:
        user_liked = ReelLike.objects.filter(user=request.user, reel=reel).exists()
    
    # Handle new comments
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = ReelCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.reel = reel
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('social_app:reel_detail', reel_id=reel.id)
    else:
        comment_form = ReelCommentForm()
    
    return render(request, 'social_app/reel/reel_detail.html', {
        'reel': reel,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked
    })

@login_required
def like_reel(request, reel_id):
    reel = get_object_or_404(Reel, id=reel_id)
    like, created = ReelLike.objects.get_or_create(user=request.user, reel=reel)
    
    if not created:
        # User already liked the reel, so unlike it
        like.delete()
        liked = False
    else:
        liked = True
    
    # Return JSON response for AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': reel.likes.count()
        })
    
    # Redirect for non-AJAX requests
    return redirect('social_app:reel_detail', reel_id=reel.id)

@login_required
def delete_reel(request, reel_id):
    reel = get_object_or_404(Reel, id=reel_id)
    
    # Check if the user is the owner of the reel
    if reel.user != request.user:
        messages.error(request, "You cannot delete someone else's reel.")
        return redirect('social_app:reel_detail', reel_id=reel.id)
    
    reel.delete()
    messages.success(request, 'Reel deleted successfully!')
    return redirect('social_app:index')
