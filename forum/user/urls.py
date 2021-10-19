from django.http import request
from django.urls import path
from . import views

urlpatterns = [
    #path('user/', views.profile, name='user'),   #r'^(?P<username>[\w.@+-]+)/$'
    path('signup/', views.Registration.as_view(), name='signup'),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name='login'),
    path('', lambda request: redirect(reverse('user'))),
]