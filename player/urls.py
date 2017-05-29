from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'player'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='player'),
    url(r'^(?P<main>(main))/$', views.main, name='main'),
    url(r'^registration/$', views.registr_user, name='registr'),
    url(r'^addroom/', views.add_room, name='add_room'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'player:player'}, name='logout'),
    url(r'^addmusic/$', views.addmusic, name='addmusic'),
    url(r'^allmusic/$', views.allMusic.as_view(), name='allmusic'),
]
