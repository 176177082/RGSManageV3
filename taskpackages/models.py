# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
from django.db import models
from users.models import User


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user/{0}/{1}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'data/{0}/{1}/{2}/{3}/{4}'.format(datetime.now().strftime("%Y"),
                                             datetime.now().strftime("%m"),
                                             datetime.now().strftime("%d"),
                                             datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), filename)


@python_2_unicode_compatible
class TaskPackage(models.Model):
    """主任务包"""
    name = models.CharField(error_messages={"unique": "任务包名称已存在"}, max_length=150, unique=True, verbose_name="任务包名称")
    owner = models.CharField(max_length=150, null=True, verbose_name=u"主版本作业员")
    exowner = models.CharField(max_length=150, null=True, verbose_name=u"前作业员")
    # TODO verbose_name=u"图号" 改为图号集
    mapnums = models.CharField(max_length=65536, null=True, verbose_name=u"图号")
    # TODO nums改为mapnumcounts,verbose_name 图幅数
    nums = models.IntegerField(default=0, verbose_name=u"任务包数量")
    file = models.FileField(upload_to=user_directory_path, null=True, verbose_name=u"任务包文件")
    status = models.CharField(max_length=10, default='0', verbose_name=u"任务包状态")
    # TODO max_length=200 200有点小，改大一些，1000
    describe = models.CharField(max_length=200, null=True, verbose_name=u"描述信息")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")
    isdelete = models.BooleanField(default=False, verbose_name=u"逻辑删除")

    class Meta:
        verbose_name = u"任务包"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TaskPackageSon(models.Model):
    """子任务包"""
    taskpackage_name = models.CharField(max_length=150, null=True, verbose_name=u"主任务包名称")
    user_username = models.CharField(max_length=150, null=True, verbose_name=u"作业员")  # 子版本上传者
    version = models.CharField(max_length=100, null=True, blank=True, verbose_name=u"子任务包版本号")
    file = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name=u"任务包文件")
    # TODO max_length=200 200有点小，改大一些，1000
    describe = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"描述信息")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name=u"更新时间")
    isdelete = models.BooleanField(default=False, verbose_name=u"逻辑删除")

    class Meta:
        verbose_name = u'子任务包'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version


@python_2_unicode_compatible
class TaskPackageOwner(models.Model):
    """任务包拥有者"""
    taskpackage_name = models.CharField(max_length=150, null=True, verbose_name=u"主任务包名称")
    owner = models.CharField(max_length=150, verbose_name=u"作业员")
    exowner = models.CharField(max_length=150, null=True, blank=True, verbose_name=u"前作业员")
    describe = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"文件描述")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name=u"创建时间")
    isdelete = models.BooleanField(default=False, verbose_name=u"逻辑删除")

    class Meta:
        verbose_name = u'任务包归属'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner