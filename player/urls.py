from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'player'
urlpatterns = [
    url(r'^$', views.index, name='player'),
    url(r'^(?P<main>(main))/$', views.main, name='main'),
    url(r'^login/$', auth_views.login, {'template_name': 'player:main'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'player:player'}, name='logout'),
    url(r'^addmusic/$', views.addmusic, name='addmusic'),
    url(r'^allmusic/$', views.allMusic.as_view(), name='allmusic'),
]
