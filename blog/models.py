# blog/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def get_authors(self):
        User = get_user_model()
        # Get the users who are authors of this queryset
        return User.objects.filter(blog_posts__in=self).distinct()

    #def get_post_with_most_comment(self):
    #    posts = Post.objects.annotate(total_comments=Count('comments'))
    #    return posts.order_by('-total_comments')
    def get_topic_with_most_post(self):
        topics = Topic.objects.annotate(total_posts=Count('blog_posts'))
        return topics.order_by('-total_posts')


class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True  # No duplicates!
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )
    slug = models.SlugField(
        null=False,
        help_text='The date & time this article was published',
        unique_for_date='published',  # Slug is unique for publication date
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )
    objects = PostQuerySet.as_manager()
    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()  # The current datetime with timezone
    class Meta:
        # Sort by the `created` field. The `-` prefix
        # specifies to order in descending/reverse order.
        # Otherwise, it will be in ascending order.
        ordering = ['-created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    #approved = models.BooleanField(default=False)
    approved_comment = models.BooleanField(default=False)
    ##################################################
    def approved(self):
        return self.Comment.objects.filter(approved_comment=True)
    ###################################################

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
########################
