# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User,Address,AddressManager
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
#from django.views.generic import Views
from django.views.generic.base import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate, login,logout
import re
from utils.mixin import LoginRequireMinxin
def register(request):
    if request.method == "GET":
        return render(request,"register.html")
    else:
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        # 2.数据校验
        if not (username and password and email):
            return render(request, 'register.html', {"errormsg": "数据不完整"})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {"errormsg": "邮箱不正确"})
        if allow != "on":
            return render(request, "register.html", {"errormsg": "请同意协议"})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 3.业务逻辑处理
        user = User.objects.create_user(username, password, email)
        user.is_actives = 0
        user.save()
        # 4.返回应答,跳转到首页
        # return redirect(reverse("goods:index"))
        return HttpResponseRedirect('/')
def register_handle(request):
    #进行注册处理
    #1.接受数据
    username = request.POST.get("user_name")
    password = request.POST.get("pwd")
    email = request.POST.get("email")
    allow = request.POST.get("allow")
    #2.数据校验
    if not (username and password and email):
        return render(request,'register.html',{"errormsg":"数据不完整"})
    #校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {"errormsg": "邮箱不正确"})
    if allow !="on":
        return render(request,"register.html",{"errormsg":"请同意协议"})

    # 校验用户名是否重复
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 用户名不存在
        user = None

    if user:
        # 用户名已存在
        return render(request, 'register.html', {'errmsg': '用户名已存在'})

    #3.业务逻辑处理
    user = User.objects.create_user(username,password,email)
    user.is_actives = 0
    user.save()
    #4.返回应答,跳转到首页
    #return redirect(reverse("goods:index"))
    return HttpResponseRedirect('/')

class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        # 进行注册处理
        # 1.接受数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")
        # 2.数据校验
        if not (username and password and email):
            return render(request, 'register.html', {"errormsg": "数据不完整"})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {"errormsg": "邮箱不正确"})
        if allow != "on":
            return render(request, "register.html", {"errormsg": "请同意协议"})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 用户名已存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 3.业务逻辑处理
        user = User.objects.create_user(username, email, password)
        user.is_actives = 0
        user.save()

        # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
        # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()

        subject = "天天生鲜欢迎您"
        message = ""
        sender = settings.EMAIL_FROM
        receiver = [email]

        html_massage ="<h1>%s,欢迎成为天天生鲜的会员</h1>请点击下面的链接激活账户<br/><a href='http://127.0.0.1:8000/users/active/%s'>http://127.0.0.1:8000/users/active/%s</a>"%(username,token,token)


        #发送邮件
        send_mail(subject,message,sender,receiver,html_message=html_massage)
        #send_register_active_email.delay(email, username, token)
        # 4.返回应答,跳转到首页
        #return redirect(reverse("goods:index"))

        return HttpResponseRedirect('/users/login')

class ActiveView(View):
    def get(self,request,token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取待激活用户的id
            user_id = info['confirm']

            # 根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('users:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已过期')

class LoginView(View):
    def get(self,request):
        print(555555555)
        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not(username and password):
            print (username)
            print(password)
            print(2222)
            return render(request,"login.html",{'errmsg':'数据不完整'})

        # 业务处理:登录校验

        # users = User.objects.get(username=username,password=password)
        #         # print(users)

        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的登录状态
                login(request, user)
                #获取登录后要跳转的地址，默认返回购物车首页
                nexl_url = request.GET.get("next",reverse("goods:index"))
                # 跳转到首页
                response = redirect(nexl_url) # HttpResponseRedirect
                #response = redirect(reverse('goods:index'))
                print("2222")
                # 判断是否需要记住用户名
                remember = request.POST.get('remember')

                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                # 返回response
                return response
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg':'账户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg':'用户名或密码错误'})

#/users
class UserInfoView(LoginRequireMinxin,View):
    #"用户中心-信息页"
    def get(self,request):
        '''显示'''
        # Django会给request对象添加一个属性request.user
        # 如果用户未登录->user是AnonymousUser类的一个实例对象
        # 如果用户登录->user是User类的一个实例对象
        # request.user.is_authenticated()

        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        return render(request,"user_center_info.html",{"page":"users",'address':address})


#/users/order
class UserOrderView(LoginRequireMinxin,View):
    # "用户中心-订单页"
    def get(self,request):
        return render(request,"user_center_order.html",{"page":"order"})

#/users/address
class AddressView(LoginRequireMinxin,View):
    # "用户中心-地址页"
    def get(self,request):
        user = request.user
        #获取用户的默认收货地址
        # try:
        #     address = Address.objects.get(user=user, is_default=True) # models.Manager
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None

        address = Address.objects.get_default_address(user)
        return render(request,"user_center_site.html",{'page':'address', 'address':address})

    def post(self,request):
        '''地址的添加'''
        # 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 校验数据
        if not all(receiver and addr and phone):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})
            # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})

        # 业务处理：地址添加
        # 如果用户已存在默认收货地址，添加的地址不作为默认收货地址，否则作为默认收货地址
        # 获取登录用户对应User对象

        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None
        address = Address.objects.get_default_address(user)
        if address:
            is_default = False
        else:
            is_default = True

        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 返回应答,刷新地址页面
        return redirect(reverse('users:address'))  # get请求方式

# /users/logout
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        '''退出登录'''
        # 清除用户的session信息
        logout(request)

        # 跳转到首页
        return redirect(reverse('goods:index'))