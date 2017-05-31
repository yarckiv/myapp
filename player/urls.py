from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='player'),
    url(r'^index/(sdfs)/$', views.Index.as_view(), name='player'),


    url(r'^addroom/', views.add_room, name='add_room'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^registration/$', views.registr_user, name='registr'),

    url(r'^logout/$', auth_views.logout, {'next_page': 'player:player'}, name='logout'),
    url(r'^(?P<main>(main))/$', views.Main.as_view(), name='main'),
    url(r'^addmusic/$', views.addmusic, name='addmusic'),
    url(r'^allmusic/$', views.allMusic.as_view(), name='allmusic'),
]
