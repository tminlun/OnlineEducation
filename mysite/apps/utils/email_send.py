#__file__ : email_send.py 
__author__: '田敏伦'
__date__: '2018/12/12 0012 20:32'

from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from mysite.settings import EMAIL_FROM


def random_str(randomlength=8):
    """
    :设置随机字符串，字符串为8位数
    逻辑：1、定义一个空字符串str；
    2、定义A - 9 的随机字符名为chars；获取到此长度（len(chars) - 1）
    3、实例化随机函数；遍历（randomlength）次，从而获取到randomlength个字符串；
    5、在chars 里面随机生成一个数字（随机数为5,那么它会在chars选择'c），赋值给strs
    6、最后返回随机字符串 str
    :return: str
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'#生成所有字符和数字
    length = len(chars) - 1 #chars的长度
    randow = Random()#实例化随机函数
    for i in range(randomlength):
        # 随机生成长度为length的数字，这些随机数在chars里面选（加入随机数为5,那么它会在chars选择'c'），最后放在str里
        str += chars[randow.randint(0, length)]
    return str #返回随机数


#email（用户的邮箱）,send_type=''（默认发送的类型）
def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()#实例化
    code = random_str(16) #生成长度为16的验证码(随机字符串)
    email_record.code = code #储存在数据库的email_record.code
    email_record.email = email #views（用户输入）传递过来的邮箱
    email_record.send_type = send_type #默认发送类型为注册(register)
    email_record.save() #code先保存在数据库
    email_title = ""
    email_body = ""
    #判断发送类型
    if send_type == "register":
        email_title = "dream网注册链接"
        email_body = "请点击下面链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        #Django自带的发送邮箱,"Django"不会自动发送邮箱，必须配置自己的邮箱，Django帮我们登录这个邮箱，通过这个邮箱帮我们发送邮件
        # subject(标题), message(内容), from_email(发送邮箱者), recipient_list：用户的邮箱 / 收件人（list）)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 会返回一个值（true / false）
        #如果邮箱发送出去了
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "dream网找回密码链接"
        email_body = "请点击下面链接找回密码:http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status: #debug：send_status = 1说明发送成功
            pass