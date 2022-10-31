from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import ImageCodeView,TestView,SmsCodeView


urlpatterns = [
    path('image_codes/<str:uuid>/',ImageCodeView.as_view()),
    path('sms_codes/<str:uuid>/',SmsCodeView.as_view()),
    #path('test/',TestView.as_view()),
]
