from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(),name='register'),
    # 用来处理ajax请求，判断用户名是否重复注册
    path('<str:username>/count/', views.UsernameCount.as_view()),
    # 用 户 登 陆
    path('login/', views.LoginView.as_view(),name='login'),
    # 用 户退出登陆
    path('logout/', views.LogoutView.as_view(),name='logout'),
    # 用户中心
    path('info/', views.UserInfos.as_view(),name='info'),
]