# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from taskpackages.models import TaskPackage, TaskPackageSon, TaskPackageOwner
from utils.permission import AdminPerssion, UserPerssion
from .serializers import TaskPackageSerializer, TaskPackageSonSerializer, TaskPackageOwnerSerializer


# TODO 命名写到具体的VIEWS上，例如这个改为TaskPackagePagination
class MyPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 50
    page_query_param = 'page'


class MyPageNumberPagination1(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 10
    page_query_param = 'page'


class TaskPackageViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    list: 查询所有任务包
    create: 划分任务包
    """
    pagination_class = MyPageNumberPagination
    serializer_class = TaskPackageSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), AdminPerssion()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            if user.isadmin:
                return TaskPackage.objects.filter(isdelete=False)
            else:
                return TaskPackage.objects.filter(isdelete=False, owner=user.username)
        return None

        # return TaskPackage.objects.filter(isdelete=False)


class TaskPackageSonViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    list:根据主任务包名字,返回左右子任务包
    create:上传子任务包
    """
    pagination_class = MyPageNumberPagination1
    permission_classes = [IsAuthenticated]
    serializer_class = TaskPackageSonSerializer

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            taskpackage_name = self.request.query_params.get("taskpackage_name")
            try:
                taskpackage = TaskPackage.objects.get(name=taskpackage_name)
            except TaskPackage.DoesNotExist:
                return []
            else:
                if user.isadmin:
                    return TaskPackageSon.objects.filter(isdelete=False, taskpackage_name=taskpackage.name)
                else:
                    if user.username == taskpackage.owner:
                        return TaskPackageSon.objects.filter(isdelete=False, taskpackage_name=taskpackage.name)
                    else:
                        return []
        return None
        # return TaskPackageSon.objects.filter(isdelete=False)


class TaskPackageOwnerViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    list: 获取@记录
    create: @功能
    """
    # permission_classes = [IsAuthenticated, AdminPerssion]
    pagination_class = MyPageNumberPagination1
    serializer_class = TaskPackageOwnerSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAuthenticated()]

        return [IsAuthenticated(), AdminPerssion()]

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            taskpackage_name = self.request.query_params.get("taskpackage_name")
            try:
                taskpackage = TaskPackage.objects.get(name=taskpackage_name)
            except TaskPackage.DoesNotExist:
                return []
            else:
                if user.isadmin:
                    return TaskPackageOwner.objects.filter(isdelete=False, taskpackage_name=taskpackage.name)
                else:
                    return TaskPackageOwner.objects.filter(owner=user.username, taskpackage_name=taskpackage.name,
                                                           isdelete=False)
        return None
