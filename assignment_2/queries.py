from django.contrib.auth import get_user_model
from django.db.models import Sum, Q ,Count

from blog.models import Comment, Post

User = get_user_model()



def question_1_return_active_users():
    """
    Return the results of a query which returns a list of all
    active users in the database.
    """

    return User.objects.filter(is_active=True)


def question_2_return_regular_users():
    """
    Return the results of a query which returns a list of users that
    are *not* staff and *not* superusers
    """
    return User.objects.filter(is_staff=False,is_superuser=False)


def question_3_return_all_posts_for_user(user):
    """
    Return all the Posts authored by the user provided. Posts should
    be returned in reverse chronological order from when they
    were created.
    """
    return Post.objects.filter(author=user)


def question_4_return_all_posts_ordered_by_title():
    """
    Return all Post objects, ordered by their title.
    """
    #list_post =list(Post.objects.all())
    #return sorted(list_post,key=lambda customer:customer.title)
    return Post.objects.all().order_by('title')


def question_5_return_all_post_comments(post):
    """
    Return all the comments made for the post provided in order
    of last created.
    """
    return Comment.objects.all().order_by('-created').filter(post = post)



def question_6_get_approved_comments_from_queryset():
    """
    Implement a queryset method on the Comment model called
    `approved` which only returns comments which have approved
    set to `True`. Do not modify the code in this function – make the
    test pass.
    """
    Comment = apps.get_model('blog', 'Comment')
    return Comment.objects.approved()


def question_7_text_search_post_text(expression):
    """
    Using the `expression` argument, return all posts containing
    this expression in their content or title. Make the query
    case-insensitive
    """
    return Post.objects.filter(Q(content__icontains=expression)| Q(title__icontains=expression))


def question_8_return_the_post_with_the_most_comments():
    """
    Return the Post object containing the most comments in
    the database. Do not concern yourself with approval status;
    return the object which has generated the most activity.
    """
    posts = Post.objects.annotate(total_comments=Count('comments'))
    return posts.order_by('-total_comments').first()


def question_9_create_a_comment(post):
    """
    Create and return a comment for the post object provided.
    """
    #user = User.objects.get(username='jianyingsheng')
    comment = Comment.objects.create(post= post,name='jianying', email = 'dorawaterloo@gmail.com',body='test this')
    return comment



def question_10_set_approved_to_false(comment):
    """
    Update the comment record provided and set approved=False
    """

    return comment.update(approved_comment = False)



def question_11_delete_post_and_all_related_comments(post):
    """
    Delete the post object provided, and all related comments.
    """
    return post.delete()
