from django.contrib.sitemaps import Sitemap
from .models import Post



class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    '''
    The changefreq and priority attributes indicate the change frequency of our
    post pages and their relevance in our website (maximum value is 1)
    '''

    def items(self):
        return Post.published.all()
    '''
    The items() method returns the QuerySet of objects to include in this sitemap. 
    By default, Django calls the get_absolute_url() method on each object to retrieve its URL
    
    If you want to specify the URL for each object, you can
    add a location method to your sitemap class
    '''

    def lastmod(self, obj):
        return obj.publish

    '''
    The lastmod method receives each object returned by items() and returns the last time 
    the object was modified. Both changefreq and priority method can also be either methods
    or attributes
    
    
    The URL for each post has been built calling its get_absolute_url() method.
The lastmod attribute corresponds to the post publish date field as we specified
in our sitemap, and the changefreq and priority attributes are also taken from
our PostSitemap class. You can see that the domain used to build the URLs is
example.com . This domain comes from a Site object stored in the database. This
default object has been created when we synced the sites framework with our
database
    
    
    '''