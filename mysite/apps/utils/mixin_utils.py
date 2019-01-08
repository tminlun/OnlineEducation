# _*_ encoding:utf-8 _*_
#__file__ : mixin_utils.py 
__author__: '田敏伦'
__date__: '2018/12/29 0029 21:00'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#用函数方式写的话直接加个装饰器（@login_required）就可以，但是我们是用类的方式写的，必须用继承的方式super
class LoginRequiredMixin(object):
    """
    在django中已Mixin结尾的，就代表最基本的View
    """
    @method_decorator(login_required(login_url="/login/", redirect_field_name='/course_detail/'))
    # 固定写法
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,*args,**kwargs)