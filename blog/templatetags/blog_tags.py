from django import template
from ..models import Post
from django.db.models import Count
from taggit.models import Tag
register= template.Library()
@register.simple_tag #simple_tag : Processes the data and returns a string
def total_post():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_post.html') #Processes the data and returns a rendered template
def get_latest_post(count=5):

    '''
    Using an inclusion tag, we
    can render a template with context variables returned by template tag
    '''
    latest_posts=Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}



@register.assignment_tag    #Processes the data and sets a variable in the context
def get_most_commented_post(count=5):

    return Post.published.annotate(total_comment=Count('comments')).order_by('-total_comment')[:count]




@register.assignment_tag
def get_all_tags():
    list_all_tags= Tag.objects.all()
    return {'list_all_tags':list_all_tags}