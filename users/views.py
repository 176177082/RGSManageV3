# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from utils.permission import AdminPerssion
from models import User
from .serializers import UserSerializer,UserListSerializer


# class UserViewSet(ReadOnlyModelViewSet):
#     """
#     list: 获取作业员列表
#     retrieve: 获取用户信息
#     """
#     serializer_class = UserSerializer
#
#     def get_permissions(self):
#         if self.action == 'list':
#             return [IsAuthenticated(), AdminPerssion()]
#         else:
#             return [IsAuthenticated()]
#
#     def get_queryset(self):
#         user_id = self.kwargs["pk"]
#         if self.action == 'list':
#             return User.objects.filter(isadmin=False)
#         else:
#             return User.objects.filter(id=user_id)
#
#         # return User.objects.all()


# 加了创建用户的功能
# class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
#     """
#     list: 获取作业员列表
#     retrieve: 获取用户信息
#     create: 创建用户
#     """
#     serializer_class = UserSerializer
#
#     def get_permissions(self):
#         if self.action == 'list' or self.action == "create":
#             return [IsAuthenticated(), AdminPerssion()]
#         else:
#             return [IsAuthenticated()]
#
#     def get_queryset(self):
#         if self.action == 'list':
#             return User.objects.filter(isadmin=False)
#         elif self.action == 'retrieve':
#             user_id = self.kwargs["pk"]
#             return User.objects.filter(id=user_id)
#         else:
#             return None
#
#
#         # return User.objects.all()


class UserListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """
    list: 获取作业员列表
    create: 创建用户
    """
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, AdminPerssion]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(isadmin=False)
        else:
            return None

        # return User.objects.all()



class UserViewSet(mixins.ListModelMixin,GenericViewSet):
    """
    list: 根据token返回用户信息
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)
