from django.conf.urls import patterns, url

# from news import views

urlpatterns = patterns('news.views',
    url(r'^$', 'IndexView', name='index'),
    url(r'^login/$', 'LoginView', name='login'),
    url(r'^logout/$', 'logoutView', name='logout'),
    url(r'^reportnews/$', 'reportnewsView', name='reportnews'),
    url(r'^(?P<category>\w+)/$', 'categoryView', name='categorynews'),
    url(r'^(?P<category>\w+)/(?P<news_title>[\w|\W]+)/$', 'detailView', name='detailnews'),
    
)

