from django.urls import path
from .views import QQAuthURLView




urlpatterns = [
    path('qq/login/',QQAuthURLView.as_view(), name='index'),
]




