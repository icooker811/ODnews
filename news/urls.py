from django.conf.urls import patterns, url

# from news import views

urlpatterns = patterns('news.views',
    url(r'^$', 'IndexView', name='index'),
    url(r'^reportnews/$', 'reportnewsView', name='reportnews'),
    url(r'^(?P<category>\w+)/(?P<news_id>\d+)/(?P<news_title>[\w|\W]+)/edit/$', 'editView', name='editnews'),
    url(r'^(?P<category>\w+)/(?P<news_id>\d+)/(?P<news_title>[\w|\W]+)/delete/$', 'deleteView', name='deletenews'),
    url(r'^(?P<category>\w+)/(?P<news_id>\d+)/(?P<news_title>[\w|\W]+)/$', 'detailView', name='detailnews'),
    url(r'^(?P<category>\w+)/$', 'categoryView', name='categorynews'),
    
)

