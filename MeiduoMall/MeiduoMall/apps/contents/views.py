from django.shortcuts import render
from django import http
from django.views import View

# Create your views here.
class IndexView(View):
    """网站首页内容"""

    def get(self,request):

        return render(request,'index.html')