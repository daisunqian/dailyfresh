# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from . import views
from .views import IndexView

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', IndexView.as_view(), name='index'),
]