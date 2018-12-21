# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RGSManageV3.settings")
import django
django.setup()


# Create your tests here.

from taskpackages.models import TaskPackageSon,TaskPackage


from django.test import TestCase
from users.models import User
from rest_framework.test import APIRequestFactory
# 强制验证
from rest_framework.test import force_authenticate
from rest_framework_jwt.views import obtain_jwt_token
from taskpackages.views import TaskPackageViewSet




if __name__ == '__main__':
    # factory = APIRequestFactory()
    # view = TaskPackageViewSet
    # user = User.objects.get(username='root')
    # request = factory.post("/v3/taskpackages/",format="json")
    # force_authenticate(request,user=user)
    # response = view(request)
    # print response


    #
    # from rest_framework.test import force_authenticate
    #
    # factory = APIRequestFactory()
    # user = User.objects.get(username='root')
    # from .views import UserViewSet
    # view = UserViewSet.as_view()
    #
    # # Make an authenticated request to the view...
    # request = factory.get('/users/')
    # force_authenticate(request, user=user)
    # response = view(request)
    #
    # print response
    #
    # from taskpackages.models import TaskPackage
    #
    # ts = TaskPackage.objects.get(id =1)
    # print ts

    # import requests
    # import json
    #
    # data = {"username": "root", "password": "root12345"}
    # response = requests.post("http://192.168.3.113:8000/v3/login", data=data)
    # json_data = json.dumps(response.content)
    # print json_data

    # taskpackage = TaskPackage.objects.filter(id = 20).first()
    # taskpackagesons =TaskPackageSon.objects.filter(isdelete=False, taskpackage_name=taskpackage.name)
    # print taskpackagesons
    pass