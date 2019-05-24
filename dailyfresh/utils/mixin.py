# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         mixin
# Description:  
# Author:sqdai
# Date:         2019/5/8
#-------------------------------------------------------------------------------

from django.contrib.auth.decorators import login_required

class LoginRequireMinxin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequireMinxin,cls).as_view(**initkwargs)
        return login_required(view)