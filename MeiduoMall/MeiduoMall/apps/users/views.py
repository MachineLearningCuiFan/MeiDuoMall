from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django import http
import re
from .models import User
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
from MeiduoMall.util.response_code import RETCODE
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


# 用户中心视图
class UserInfos(LoginRequiredMixin,View):

    def get(self,request):
        """提供用户中心函数
        如果用户登陆就直接进入用户中心，如果用户未登陆则进入用户登陆界面，且用户登陆完成之后直接进入用户中心
        """
        # 第一种方式
        # if request.user.is_authenticated:
        #     return render(request,'user_center_info.html')
        # else:
        #     return redirect(reverse('users:login'))

        # 第二种实现方式

        #self.redirect_field_name = reverse('users:info')
        return render(request,'user_center_info.html')

# 用户退出登陆
class LogoutView(View):

    def get(self,request):
        """实现用户退出的逻辑"""
        # 清除状态保持信息
        logout(request)
        response = redirect(reverse('contents:index'))
        # 删除cookie 中username
        response.delete_cookie('username')
        return response


#  用户登录
class LoginView(View):
    def get(self,request):
        """提供用户登陆界面"""

        return render(request, 'login.html')

    def post(self,request):
        """实验用户登陆逻辑"""
        # 第一步、接受参数
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        remembered = request.POST.get("remembered")
        # 第二步、校验参数
        if not all([username,password]):
            return http.HttpResponseForbidden("缺少必要参数")
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
            # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')

        # 第三步、认证用户:使用用户名是否存在，如果用户存在，在校验密码是否正确
        # user = User.objects.get(username=username)
        # user.check_password(password)
        user = authenticate(username=username,password=password)
        if user is None:
            return render(request,'login.html',{'account_errmsg':'用户账号或密码错误'})

        # 第四步、状态保持
        login(request,user)
        # 使用remenbered 来选择状态保持时间
        if remembered != 'on':
            # 没有保存密码，浏览器回话结束后就销毁
            request.session.set_expiry(0)
        else:# 保存密码，默认是两周
            request.session.set_expiry(None)

        # 第五步、响应结果:登陆成功，重定向到首页
        next = request.GET.get('next')
        if next:
            return redirect(next)
        else:
            response = redirect(reverse('contents:index'))
            ## 为了实现在首页右上角显示出用户名信息，我们需要将用户名缓存到cookie中
            #response.set_cookie('key','value','过期时间')
            response.set_cookie('username',user.username,max_age=3600*24*15)

            return response



# 用来判断用户名是否重复
class UsernameCount(View):
    def get(self,request,username):
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code':RETCODE.OK,'errmsg':'ok','count':count})



#  用户注册
class RegisterView(View):
    def get(self,request):
        print(request)
        '''提供用户注册页面'''
        #return HttpResponse("nie1")
        return render(request,"register.html")

    def post(self,request):
        """实现用户注册逻辑"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')

        # 判断参数是否齐全
        if not all([username,password,password2,mobile,allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        #create_user 返回用户对象
        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            return render(request,"register.html",{'register_error_message':'注册失败！请重新注册'})

        # 状态保持
        login(request,user)

        # 第五步、响应结果:登陆成功，重定向到首页
        response = redirect(reverse('contents:index'))

        ## 为了实现在首页右上角显示出用户名信息，我们需要将用户名缓存到cookie中
        # response.set_cookie('key','value','过期时间')
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response






