from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from django.utils.translation import ugettext as _
from django.conf import settings



class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,primary_key=True, unique=True, related_name='profile')

    date_of_birth=models.DateField(blank=True,null=True)
    about_author=models.TextField(max_length=100)
    photo=models.ImageField(upload_to='upload/users/%Y/%m/%d',blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),)
    # tagbase=TagBase()
    # tag_name=tagbase.name
    #user=models.ForeignKey(SiteUser, related_name='post')
    title = models.CharField(max_length=250)

    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(Profile, related_name='blog_posts')
    # about_author=models.CharField(max_length=30)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                            choices=STATUS_CHOICES,
                            default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    published=PublishedManager()
    tags=TaggableManager()

    #The tags manager will allow you to add, retrieve, and remove tags from Post objects


    def get_absolute_url(self):

        return reverse('blog:post_detail',args=[self.publish.year,
                                                self.publish.strftime('%m'),
                                                self.publish.strftime('%d'),
                                                self.slug,

                                                ])






class Comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments')
    name=models.CharField(max_length=50)
    email=models.EmailField()
    body=models.TextField(max_length=250)
    updated=models.DateTimeField(auto_now_add=True)
    created=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    # img=models.ImageField(max_length=1024)

    class Meta:
        ordering='created',

    def __str__(self):
        return '{} commented on {}'.format(self.name,self.post)


class PostImage(models.Model):
    post = models.ForeignKey(Post, null=True, blank=True,verbose_name=_("Post"), related_name='images')
    image = models.ImageField(max_length=1024, upload_to='upload/blog/image/%Y/%m/%d/', null=True, blank=True)
    image_description = models.TextField( blank=True,null=True,help_text="name of image/small description")
    image_title = models.CharField(max_length=50, blank=True,null=True,help_text="title of image/small description")


    def __str__(self):
        return self.image_title



class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(max_length=50, blank=False)
    phone=models.CharField(max_length=10,blank=False)
    query=models.TextField(max_length=200)


# class Subscribers(models.Model):
#     date_join=models.DateField(auto_now=True)
#     email=models.EmailField()