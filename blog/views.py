# blog/views.py

from django.shortcuts import render
from . import models


def home(request):
    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    authors = models.Post.objects.get_authors()
    popular_comments = models.Post.objects.get_post_with_most_comment()
    # Add as context variable "latest_posts"
    context = {
        'authors': authors,
        'latest_posts': latest_posts,
        'popular_comments': popular_comments
    }
    return render(request, 'blog/home.html', context)
