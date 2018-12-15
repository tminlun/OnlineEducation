from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate,login
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm
# Create your views here.


class CustomBackend(ModelBackend):
    """
    #邮箱和用户名都可以登录
    # 基础ModelBackend类，因为它有authenticate方法
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    """登录"""
    def get(self,request):
        login_form = LoginForm()
        return render(request, 'login.html', {
            'login_form': login_form,
        })
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            # 判断数据库账号密码是否一致
            if user is not None:
                #判断用户是否激活，即使注册了，没激活，也不给登录
                if user.is_active: #(user.is_active == True)
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    #返回表单后，用户之前输入错误的账号密码还会保留在框中
                    return render(request, 'login.html', {'msg': '用户为激活', 'login_form': login_form})
            else:
                return render(request,'login.html', {'msg': '用户或者密码错误'})#查询数据库出错，返回自己定义的错误，不用返回表单
        else:
            # 直接返回表单自带的错误，所以要返回表单
            return render(request, 'login.html', {'login_form': login_form})


class ActiveUserView(View):
    """激活注册码,运行此URL就会激活"""
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code) #筛选符合条件的“EmailVerifyRecord”对象
        # 如果有此链接
        if all_record:
            for record in all_record: #遍历出每一个符合这个条件的对象（record是单个对象）
                email = record.email #获取对象的具体邮箱
                user = UserProfile.objects.get(email=email) #获取此验证码和邮箱的用户
                user.is_active = True #用户点击（urls：user_active）后，激活
                user.save() #保存
        else:
            return render(request, 'active_fail.html') #验证码输入错误
        return render(request, 'login.html')#激活成功（打开url页面）返回登录页面


class RegisterView(View):
    """用户注册"""
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{
            'register_form': register_form,
        })
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', '')
            user_email = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            pass_word_again = request.POST.get('password_again', '')
            # 判断
            if UserProfile.objects.filter(username=user_name):
                return render(request,'register.html',{'register_form': register_form, 'msg': '用户名已存在'})
            if UserProfile.objects.filter(email=user_email):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户邮箱已存在'})
            if pass_word != pass_word_again:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '两次输入不一致'})

            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_email
            user_profile.password = make_password(pass_word_again)# 对注册的密码加密
            user_profile.is_active = False #让用户手动激活,默认为为激活
            user_profile.save()# 然后保存
            send_register_email(user_email, 'register')# 发送邮箱,注册类型
            return render(request, 'login.html')#注册完跳到登录页面
        #表单自动验证错误
        else:
            return render(request, 'register.html', {
                'register_form': register_form
            })


class ForgetPwdView(View):
    """
    忘记密码
    逻辑：1、验证表单；
    2、获取到邮箱（email）传递给send_register_email从而发送邮箱
    """
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, 'forget')#发送邮箱
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})


class ResetView(View):
    """
    忘记密码激活
    逻辑：1、用户点击忘记密码激活链接后，通过验证码（active_code）获取具体用户的邮箱。因为我们不知道是哪个用户，email可以获取到具体的user（用户）
    2、如果获取不到验证码，返回一个错误页面（active_fail.html）
    3、获取到邮箱后，转跳到修改密码(password_reset.html)页面,把具体邮箱传递给password_reset.html,
    4、修改完密码后，转跳到登录页面(login.html)
    """
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code) #找到所有 此链接的对象
        if all_record: #如果有此对象
            for record in all_record: #遍历所有的对象
                email = record.email #获取EmailVerifyRecord 的邮箱（email）
                return render(request, 'password_reset.html', {'email': email}) #传递具体用户的邮箱
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    重设密码
    逻辑：1、（Templates - Urls - Views）；判断forms是否规范，不规范返回错误，并且返回email（email不是用户输入的,如果不返回只有返回表单）
    2、让用户输入两次密码，获取到用户输入的密码和（激活链接的email）
    3、找到此邮箱的user，把密码（加密）赋值（重设）给user.password
    4、保存，返回登录页面
    """
    def get(self, request):
        modify_form = ModifyPwdForm()
        return render(request, 'password_reset.html', {"modify_form": modify_form})

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            #获取值
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            #判断
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "两次输入不一致"})
            #获取当前邮箱（用户名）的用户,密码保存（重设）到数据库
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2) #因为重设的密码是新密码，是要加密
            user.save()

            return redirect(reverse('login')) #重定向登录页面
        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html",{"modify_form":modify_form, "email": email})
