from django.http import request
from django.urls import path
from . import views
from django.shortcuts import redirect
from django.urls import reverse , re_path


urlpatterns = [
    path('home/', views.home, name='home'),
    re_path(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/view_topic/(?P<id>\d+)/', views.single_topic, name='view_topic'),
    path('boards/new/', views.new_board, name='new_board'),
    re_path(r'^boards/(?P<pk>\d+)/new_topic/$', views.new_topic, name='new_topic'),
    path('', lambda request: redirect(reverse('home'))),
]