import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner


#xadmin中这里是继承object，不再是继承admin
class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ('code', 'email', 'send_type', 'send_time')
    # 搜索的字段，不要添加时间搜索
    search_fields = ['code', 'email', 'send_type']
    # 过滤
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fas fa-at'


class BannerAdmin(object):
    list_display = ('title', 'image', 'url', 'index', 'add_time')
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    model_icon = 'fas fa-angle-double-left'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)


# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True  # 调用更多主题


class GlobalSettings(object):
    #修改左上角的title
    site_title = 'TML后台管理界面'
    #修改footer
    site_footer = 'TML的公司'
    #收起菜单
    menu_style = 'accordion'


# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)#views.(点)
# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)

