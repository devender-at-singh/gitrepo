"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog.sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout
sitemaps={'posts':PostSitemap}


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls',namespace='blog',app_name='blog')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
                                name='django.contrib.sitemaps.views.sitemap'),

    # '''We define a URL pattern that matches with sitemap.xml and uses the sitemap
    # view. The sitemaps dictionary is passed to the sitemap view
    #
    # we can open
    #http://127.0.0.1:8000/sitemap.xml in your browser
    #
    #
    # '''
    url(r'^contact/$','blog.views.contact', name='contact'),
    url(r'^signup/$','blog.views.signup', name='signup'),
    url(r'^signin/$','blog.views.signin', name='signin'),
    url(r'^aboutus/$','blog.views.aboutus', name='aboutus'),
    url(r'^index/$','blog.views.index',name='index'),
    url(r'^dashboard/$','blog.views.dashboard',name='dashboard'),
    url(r'^edit/$','blog.views.edit',name='edit'),
    #url(r'^password_reset','', name='password_reset'),
    url(r'^t-and-c','blog.views.tandc',name='t-and-c'),
    url(r'^logout/$', 'blog.views.logged_out',name='logout'),
    url(r'^logout-then-login/$','django.contrib.auth.views.logout_then_login',
        name='logout_then_login'),
    url(r'^change-password/$','blog.views.change_password', name='change-password'),
    url(r'^password-change/done/$','django.contrib.auth.views.password_change_done',
        name='password_change_done'),

    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
                      'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done',
                      name='password_reset_done'),
    url(r'^password-reset/compelte/$', 'django.contrib.auth.views.password_reset_complete',
                      name='password_reset_complete'),
    url(r'^subscribe/$','blog.views.subscribe',name='subscribe'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)