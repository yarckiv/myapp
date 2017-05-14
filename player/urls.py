from django.conf.urls import url

from . import views

app_name = 'player'
urlpatterns=[
    url(r'^$', views.index, name='player'),
    url(r'^(?P<main>(main))/$', views.Main.as_view(), name='main'),
    ]