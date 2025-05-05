from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post, Reel
from .forms import SearchForm

def search(request):
    form = SearchForm(request.GET)
    results = {
        'users': [],
        'posts': [],
        'reels': []
    }
    
    if form.is_valid():
        query = form.cleaned_data['query']
        
        # Search users
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
        
        # Search posts
        posts = Post.objects.filter(
            Q(content__icontains=query)
        )
        
        # Search reels
        reels = Reel.objects.filter(
            Q(description__icontains=query)
        )
        
        results = {
            'users': users,
            'posts': posts,
            'reels': reels,
            'query': query
        }
    
    return render(request, 'social_app/search/search_results.html', {
        'form': form,
        'results': results
    })
