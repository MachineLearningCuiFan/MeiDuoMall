from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from .libs.captcha.captcha import captcha
from django import http
from .constants import IMAGE_CODE_REDIS_EXPIRES
from MeiduoMall.util.response_code import RETCODE
# Create your views here.


class ImageCodeView(View):
    """图形验证码"""
    def get(self,request,uuid):
        """
        uuid : 用于标识图形验证码属于哪个用户！
        """
        # 第一步、接受参数并检测
        # 第二步、实现主体业务逻辑，生成、保存，响应图像验证码
        # 第三步、响应图形验证码

        # 利用 captcha包生成随机图片验证码
        text,image = captcha.generate_captcha()
        # 保存验证码的text 到redis数据库
        redis_conn = get_redis_connection("verifications")
        redis_conn.setex("image_%s"%uuid,IMAGE_CODE_REDIS_EXPIRES,text)

        return http.HttpResponse(image,content_type='image/jpg')



class TestView(View):
    """测试 字符串传参"""
    def get(self,requset):
        username = requset.GET.get("username")
        return http.HttpResponse(username+"srerwer")


class SmsCodeView(View):
    """短信验证码"""
    def get(self,request,uuid):
        # 校验图片验证码是否正确：
        # 1、 获取redis数据库连接对象
        redis_conn = get_redis_connection("verifications")
        # 2、 通过uuid获取redis数据库中图形验证码
        image_code_server = redis_conn.get('image_%s' % uuid)

        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码已失效'})
        # 删除图形验证码
        redis_conn.delete('img_%s' % uuid)
        # 3、 获取用户输入的 图形验证码
        image_code_client = request.GET.get("image_code")
        #  4 、对比图形验证码
        image_code_server = image_code_server.decode()
        if image_code_client.lower() != image_code_server.lower():  # 转小写，再比较
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证码有误'})
            # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})






