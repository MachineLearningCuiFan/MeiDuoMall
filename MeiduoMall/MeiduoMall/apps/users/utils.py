# 自定义用户多账号登陆
import re
from django.contrib.auth.backends import ModelBackend
from .models import User

def get_user_by_account(account):
    """
    通过用户名或者账号获取用户
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # 用户名为手机号码
            user = User.objects.get(mobile=account)
        else:  # 用户名为普通用户名
            user = User.objects.get(username=account)
    except :
        return None
    return user





# 重写django默认的账号验证后端
class UsernameMobileBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        username:可能是用户名 也可能是手机号码
        """
        # 校验username 参数是用户名还是手机号码
        user = get_user_by_account(account=username)
        # 如果用户存在，校验密码
        if user and user.check_password(password):
            return user
        else:
            return None



