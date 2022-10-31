from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import IndexView

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
]
