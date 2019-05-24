# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from django.shortcuts import render
from django.views.generic import View
from .models import GoodsType,IndexGoodsBanner,IndexTypeGoodsBanner,IndexPromotionBanner
# Create your views here.
# def index(request):
#     return render(request,"index.html")

class IndexView(View):
    def get(self,request):
        types = GoodsType.objects.all()
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')
        #type_goods_baner  = IndexTypeGoodsBanner.objects.all()
        # 获取首页分类商品展示信息
        for type in types:  # GoodsType
            # 获取type种类首页分类商品的图片展示信息
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
            # 获取type种类首页分类商品的文字展示信息
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

            # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
            type.image_banners = image_banners
            type.title_banners = title_banners
        cart_count = 0
        context = {'types': types,
                   'goods_banners': goods_banners,
                   'promotion_banners': promotion_banners,
                   #'type_goods_baner':type_goods_baner,
                   'cart_count':cart_count,}
        return render(request, "index.html",context)