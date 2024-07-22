from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('signup',signup,name='signup'),
    path('signin',signin,name='signin'),
    path('logout',logout_user,name='logout_user'),
    path('setting',setting,name='setting'),
    path('upload',upload,name='upload'),
    path('profile/<str:pk>',profile,name='profile'),
    path('follow',follow,name='follow'),
    path('search',search,name='search'),
    path('delete/<str:pk>/<str:usr>',delete_post,name='delete_post'),
]