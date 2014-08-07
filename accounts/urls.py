from django.conf.urls import patterns, url

# from news import views

urlpatterns = patterns('accounts.views',
    url(r'^login/$', 'LoginView', name='login'),
    url(r'^logout/$', 'logoutView', name='logout'),
)

