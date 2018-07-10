from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    '''The title , link , and
    description attributes correspond to the <title> , <link> , and <description>
    RSS elements respectively.'''
    title = 'blog title'
    link = '/blog link/'
    description = 'blog description.'


    def items(self):
        '''The items() method retrieves the objects to be included in the feed. We are
retrieving only the last five published posts for this feed.'''
        return Post.published.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        '''The item_title() and
item_description() methods receive each object returned by items() and return
the title and description for each item.We use the truncatewords built-in template
filter to build the description of the blog post with the first 30 words.'''
        return truncatewords(item.body, 30)