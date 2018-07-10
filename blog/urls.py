from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # post views
    url(r'^post_list/$', views.post_list, name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list,name='post_list_by_tag'),
    url(r'^(?P<post_id>\d+)/$', views.post_share,name='post_share'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<postit>[-\w]+)/$',
        views.post_detail,name='post_detail'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
    url(r'blog manager', views.post_sidebar,name='blog manager'),



    # '''
    # url(r'^$', views.post_list, name='post_list'),
    # # url(r'^$', views.PostListView.as_view(), name='post_list'),
    #
    # url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list,name='post_list_by_tag'),
    #
    # The first pattern will call the post_list view without any optional
    # parameters, while the second pattern will call the view with the tag_slug parameter.
    # '''
    ]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)