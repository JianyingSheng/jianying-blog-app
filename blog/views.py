# blog/views.py

from django.shortcuts import render
from . import models


def home(request):
    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    #authors = models.Post.objects.get_authors()
    popular_topics = models.Post.objects.get_topic_with_most_post()
    # Add as context variable "latest_posts"
    context = {
        'latest_posts': latest_posts,
        'popular_topics': popular_topics
    }
    return render(request, 'blog/home.html', context)
