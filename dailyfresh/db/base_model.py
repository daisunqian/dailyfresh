# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         base_model
# Description:  
# Author:sqdai
# Date:         2019/3/11
#-------------------------------------------------------------------------------

from django.db import models

class BaseModel(models.Model):
    """"抽象模型类"""
    create_time = models.DateTimeField(auto_now=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    is_delete = models.BooleanField(default=False,verbose_name="删除标记")

    class Meta:
        abstract = True