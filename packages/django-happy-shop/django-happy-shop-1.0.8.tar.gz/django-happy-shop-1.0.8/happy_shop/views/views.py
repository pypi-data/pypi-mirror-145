from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.
from happy_shop.models import HappyShopingCart
from happy_shop.conf import happy_shop_settings
from happy_shop.forms import HappyShopLoginForm, HappyShopRegisterForm


class BaseView:
    """全局基类视图"""
    
    title = happy_shop_settings.TITLE
    desc = happy_shop_settings.DESC
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['desc'] = self.desc
        if self.request.user.is_authenticated:
            context['cart_num'] = HappyShopingCart.get_cart_count(self.request.user)
        else:
            context['cart_num'] = 0
        return context


class HappyShopLoginView(BaseView, LoginView):
    """
    登录视图
    """
    form_class = HappyShopLoginForm
    template_name = "happy_shop/login.html"
    next_page = "happy_shop:index"
    extra_context = {
        "site_title": "登录",
    }


class HappyShopRegisterView(BaseView, FormView):
    """
    注册用户 
    """
    template_name = 'happy_shop/register.html'
    form_class = HappyShopRegisterForm
    success_url = reverse_lazy("happy_shop:index")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data.get('password'))
        new_user.username = form.cleaned_data.get('username')
        new_user.save()
        return super().form_valid(form)


class HappyShopLogoutView(BaseView, LogoutView):
    """
    Log out the user and display the 'You are logged out' message.
    """


class HappyShopUploadImage(LoginRequiredMixin, View):
    """富文本编辑器上传图片
    首先会检查项目根目录有没有media/upload/的文件夹
    如果没有就创建，图片最终保存在media/upload/目录下
    返回图片路径为 "/media/upload/file.png"
    wangEditor_v4文档：https://www.wangeditor.com/
    """
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        import os
        import uuid
        file_data = request.FILES
        keys = list(file_data.keys())
        file_path = settings.BASE_DIR / 'media/upload/'
        if os.path.exists(file_path) is False:
            os.mkdir(file_path)
        # 返回数据中需要的data
        data = []
        for key in keys:
            img_dict = {}
            file = file_data.get(f'{key}')
            # 重命名文件名称
            new_path = os.path.join(file_path, file.name) 
            names = os.path.splitext(file.name)
            names[0] = ''.join(str(uuid.uuid4()).split('-'))
            file.name = '.'.join(names)
            # 开始上传
            with open(new_path, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            # 构造返回数据
            img_dict['url'] = f'/media/upload/{file.name}'
            data.append(img_dict)
        context = {"errno": 0,"data":data}
        return JsonResponse(context)
    