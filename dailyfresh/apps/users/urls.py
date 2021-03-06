# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required
from . import views
from .views import RegisterView,ActiveView,LoginView,UserInfoView,UserOrderView,AddressView,LogoutView
urlpatterns = [
    #url(r'^register$',views.register,name="register"),
    #url(r'^register_handle$',views.register_handle,name="register_handle"),
    url(r'^register$',RegisterView.as_view(),name="register"),
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name="active"),# 用户激活
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    # url(r'^$',login_required(UserInfoView.as_view()),name="users"),
    # url(r'^order$',login_required(UserOrderView.as_view()),name="order"),
    # url(r'^address$',login_required(AddressView.as_view()),name="address")
    url(r'^$',UserInfoView.as_view(),name="users"),
    url(r'^order$',UserOrderView.as_view(),name="order"),
    url(r'^address$',AddressView.as_view(),name="address"),
]
