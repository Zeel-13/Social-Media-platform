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
    path('like_post',like_post,name='like_post'),
    path('profile/<str:pk>',profile,name='profile'),
    path('follow',follow,name='follow'),
    path('search',search,name='search'),

]