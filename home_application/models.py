# -*- coding: utf-8 -*-
from django.db import models


class Script(models.Model):
    """业务信息"""

    script_name = models.CharField(u'脚本名', max_length=50)
    script_text = models.CharField(u'脚本内容', max_length=500)
    script_input = models.CharField(u'默认参数', max_length=200, default=None, null=True)
    script_desc = models.CharField(u'脚本说明', max_length=200, default=None, null=True)


class OptLog(models.Model):
    """操作记录信息"""
    user = models.CharField(u'操作用户', max_length=128, null=True)
    start_time = models.DateField(default=None, null=True)
    biz = models.CharField(max_length=50, default=None, null=True)
    task_id = models.CharField(max_length=50, default=None, null=True)
    result = models.CharField(max_length=500, default=None, null=True)
    celery_id = models.CharField(max_length=50, default=None, null=True)
    script_id = models.IntegerField(max_length=11, default=None, null=True)
    end_time = models.DateField(default=None, null=True)
    log = models.CharField(max_length=500, default=None, null=True)
    status = models.CharField(max_length=500, default=None, null=True)
