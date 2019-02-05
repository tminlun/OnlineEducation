import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, Course, UserFavorite, UserMessage
from organization.models import CourseOrg ,Teacher
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,ModifyImageForm, UpdatePwdForm, UpdateUserForm
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
            # 可以防止sql攻击，把攻击的账号（' OR 1=1#） 的'转换为特殊字符  【密码：123(随意输入)】
            user = authenticate(username=user_name, password=pass_word)
            # 判断数据库账号密码是否一致
            if user is not None:
                #判断用户是否激活，即使注册了，没激活，也不给登录
                if user.is_active: #(user.is_active == True)
                    login(request, user)
                    return redirect('index')
                else:
                    #返回login_form后，用户之前输入错误的账号密码还会保留在框中
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
        return redirect('login', reverse('index'))#激活成功（打开url页面）返回登录页面


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
            user_profile.is_active = False #让用户手动激活,默认为未激活
            user_profile.save()# 然后保存

            user_message = UserMessage()
            user_message.user = request.user.id
            user_message.message = '恭喜您注册成功'
            user_message.save()

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


class LogoutView(View):
    """注销"""
    def get(self,request):
        logout(request)
        return redirect('index')


class UserInfoView(LoginRequiredMixin, View):
    """用户信息的 显示和修改 """
    def get(self, request):
      return render(request, 'usercenter-info.html',{})

    def post(self, request):
        update_user_form = UpdateUserForm(request.POST, instance=request.user)
        if update_user_form.is_valid():
            #cleaned_data可以获取（传递过来）的值
            nick_name = update_user_form.cleaned_data['nick_name']
            brithday = update_user_form.cleaned_data['brithday']
            gander = update_user_form.cleaned_data['gander']
            adress = update_user_form.cleaned_data['adress']
            mobile = update_user_form.cleaned_data['mobile']
            #获取当前用户
            user = request.user
            user.nick_name = nick_name
            user.brithday = brithday
            user.gander = gander
            user.adress = adress
            user.mobile = mobile
            user.save()

            return HttpResponse('{"status":"success"}', content_type="application/json,charset=utf-8")

        else:
            #出现错误
            return HttpResponse(json.dumps(update_user_form.errors), content_type="application/json,charset=utf-8")


def Success(msg):
    data = {}
    data['status'] = 'success'
    data['msg'] = msg
    return JsonResponse(data)


def Fail(msg):
    data = {}
    data['status'] = 'fail'
    data['msg'] = msg
    return JsonResponse(data)


class ModifyImageView(LoginRequiredMixin, View):
    """
    用户修改头像:
        取出form里面的数据
        image = image_form.cleaned_data['image']
        request.user.image = image
        request.user.save()

        instance=request.user：保存后form不会新增用户

    """
    def post(self, request):
        image_form = ModifyImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json,charset=utf-8")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json,charset=utf-8")


class UpdatePwdView(LoginRequiredMixin, View):
    """
    个人中心用户修改密码
    不管是异步还是from表单，都要加 csrf_token, 不然debug不了
    """
    def post(self,request):
        updatepwd_form = UpdatePwdForm(request.POST)
        if updatepwd_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')

            if password1 != password2:
                return Fail('两次输入不一致')

            user = request.user
            user.password = make_password(password2)
            user.save()
            return Success('修改成功')
        else:
            # 返回错误，不需要加"fail"；json.dumps(updatepwd_form.errors)：把错误的字典转换为字符串
            return HttpResponse(json.dumps(updatepwd_form.errors), content_type="application/json,charset=utf-8")


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    个人中心修改邮箱-获取验证码
        获取邮箱，获取验证码，进行激活


    坑：csrf_token、models长度、注册过的邮箱不能和修改相同
    """
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            # 邮箱已经被注册，返回错误信息
            return HttpResponse('{"email":"邮箱已被注册"}',content_type="application/json,charset=utf-8")
        if not send_register_email(email,'update_email'):
            send_register_email(email,'update_email')
        else:
            return HttpResponse('{"email":"已发送验证码"}', content_type="application/json,charset=utf-8")

        return HttpResponse('{"status":"success"}', content_type="application/json,charset=utf-8")


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    输入验证码（隐秘的）， 需要post
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        if EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email"):
            #刚刚发送验证码的记录：数据库有此验证码，成功
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json,charset=utf-8")

        else:

            #数据库没有此验证码和修改的邮箱
            return HttpResponse('{"email":"验证码或者邮箱错误"}', content_type="application/json,charset=utf-8")


class MyCourseView(View):
    """我的课程"""
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        #当前用户的学习课程

        return render(request, 'usercenter-mycourse.html',{
            "user_courses":user_courses,
        })


class FavCourseView(View):
    """用户收藏列表-课程"""
    def get(self, request):
        current_path = 'fav_course'
        fav_course_list = []
        #filter、all都是返回list
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            #遍历筛选的课程ID，得到每一个课程
            course_id = int(fav_course.fav_id)
            course = Course.objects.get(id=course_id)
            # id只能用在get()方法
            fav_course_list.append(course)
            #把一个个收藏课程放在列表

        #用户收藏的课程
        return render(request, 'usercenter-fav-course.html', {
            "fav_course_list": fav_course_list,
            'current_path': current_path,
        })


class FavOrgView(View):
    """用户收藏列表-机构"""
    def get(self, request):
        current_path = 'fav_org'
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            #遍历类型为机构的所有收藏记录，取到ID
            org_id = int(fav_org.fav_id)
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html',{
            "org_list": org_list,
            'current_path': current_path,
        })


class FavTeacherView(View):
    """我的收藏-讲师"""
    def get(self, request):
        current_path = 'fav_teacher'
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = int(fav_teacher.fav_id)
            teacher = Teacher.objects.get(pk=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'current_path': current_path,
        })


class MyMessageView(View):
    """用户信息列表"""
    def get(self, request):
        #获取当前用户（用户ID）的消息
        user_message = UserMessage.objects.filter(user=request.user.id)
        for message in user_message:
            message.has_read = True
            message.save()
        # 分页功能
        try:
            page = request.GET.get('page', 1)  # 获取n（page=n）,默认显示第一页
        except PageNotAnInteger:
            page = 1  # 出现异常显示第一页
        p = Paginator(user_message, 2, request=request)  # 进行分页，每5个作为一页
        messages = p.page(page)  # 获取当前页面

        return render(request, 'usercenter-message.html',{
            'messages': messages,
        })


class IndexView(View):
    """首页"""
    def get(self, request):
        all_banner = Banner.objects.all().order_by("index")# 轮播图，使用order_by("index") 升序来控制顺序

        course_banners = Course.objects.filter(is_banner=True)[:3]#课程是否为轮播图 is_banner

        courses = Course.objects.filter(is_banner=False)[:6]#不是轮播图的课程

        orgs = CourseOrg.objects.all()[:15] #机构
        return render(request, 'index.html', {
            "all_banner": all_banner,
            "course_banners": course_banners,
            "courses": courses,
            "orgs": orgs,
        })


def path_not_found(request):
    """404页面"""
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404 #设置显示状态：404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response