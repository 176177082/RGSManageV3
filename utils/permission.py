# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.permissions import BasePermission
from taskpackages.models import TaskPackage


class AdminPerssion(BasePermission):
    message = "管理员权限才可以访问"

    def has_permission(self, request, view):
        if request.user.isadmin is False:
            return False
        return True


class UserPerssion(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.username == obj.owner:
            return True

        return False




# class UserPerssion(BasePermission):
#     message = "只能访问自己的数据"
#     def has_object_permission(self, request, view, obj):
#         """
#         Return `True` if permission is granted, `False` otherwise.
#         """
#         if request.user.id == obj.id:
#             return True
#         return False