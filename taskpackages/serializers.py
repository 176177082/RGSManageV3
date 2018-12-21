# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.exceptions import APIException
from models import TaskPackage, TaskPackageSon, TaskPackageOwner
from django.conf import settings
from rest_framework import status
from celery_app.clipfromsde import clipfromsde

# TODO 命名不够具体
class MyValidationError(APIException):
    status_code = status.HTTP_403_FORBIDDEN


class TaskPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPackage
        # exclude = ('isdelete',)
        fields = ["id", "name", "owner", "exowner", "mapnums", "nums", "file", "status", "createtime", "updatetime",
                  "describe"]
        extra_kwargs = {
            "name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "owner": {"required": True, "allow_null": False, "help_text": u"作业员"},
            "exowner": {"read_only": True},
            "mapnums": {"required": True, "write_only": True,
                        "error_messages": {"required": u"请输入图号"}, "help_text": u"图号"},
            "nums": {"required": True},
            # "file": {"required": True, "allow_null": False, "error_messages": {"required": "请选择文件"},
            #          "help_text": "任务包文件"},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
            "updatetime": {"format": '%Y-%m-%d %H:%M:%S'},
            "describe": {"allow_null": False, }
        }

    def create(self, validated_data):
        taskpackage = super(TaskPackageSerializer, self).create(validated_data)

        taskpackageson = TaskPackageSon.objects.create(
            taskpackage_name=taskpackage.name,
            version="v0.0",
            describe=taskpackage.describe,
            user_username=taskpackage.owner,
            file=taskpackage.file
        )

        MEDIA = settings.MEDIA_ROOT
        mapnumlist = validated_data["mapnums"]
        taskname = validated_data["name"]
        # user_id = self.context["request"].user.id
        # TODO 此处加一注释，提醒进入celery进行异步处理
        clipfromsde.delay(mapnumlist, MEDIA, taskname, taskpackage.id, taskpackageson.id)

        return taskpackage


class TaskPackageSonSerializer(serializers.ModelSerializer):
    handle_progress = serializers.BooleanField(allow_null=True)
    taskpackage_file_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = TaskPackageSon
        # exclude = ('isdelete',)
        fields = ["taskpackage_name", "version", "createtime", "updatetime", "describe", "file", "user_username",
                  "handle_progress", "taskpackage_file_id"]
        extra_kwargs = {
            "taskpackage_name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "user_username": {"read_only": True, "help_text": u"子任务包归属者"},
            "version": {"read_only": True},
            "file": {"required": True, "allow_null": False, "error_messages": {"required": u"请选择文件"}},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
            "updatetime": {"format": '%Y-%m-%d %H:%M:%S'},
            # "handle_progress":{"required": False},
            # "taskpackage_file_id":{"required": False}

        }

    def validate(self, validated_data):

        taskpackage_name = validated_data.get("taskpackage_name")
        try:
            taskpackage = TaskPackage.objects.filter(name=taskpackage_name, isdelete=False).first()
        except TaskPackage.DoesNotExist:
            raise serializers.ValidationError(u"任务包{}不存在".format(taskpackage_name))
        else:
            user = self.context["request"].user
            # 只有管理员和主任务包拥有者才能上该任务包的子版本
            if not user.isadmin and user.username != taskpackage.owner:
                raise MyValidationError(u"用户{}无权限".format(user.username))

            validated_data["user_username"] = user.username
            validated_data["taskpackage"] = taskpackage

        return validated_data

    def create(self, validated_data):
        taskpackage = validated_data["taskpackage"]
        # taskpackagesons = TaskPackageSon.objects.filter(taskpackage_name=taskpackage_name)
        # version = "v" + str(len(taskpackagesons) + 1)+".0"
        taskpackageson_nums = TaskPackageSon.objects.filter(taskpackage_name=taskpackage.name).count()
        # version = "v" + str(taskpackageson_nums + 1) + ".0"
        version = "v" + str(taskpackageson_nums) + ".0"

        taskpackageson = TaskPackageSon.objects.create(
            taskpackage_name=validated_data["taskpackage_name"],
            user_username=validated_data["user_username"],
            version=version,
            file=validated_data["file"],
            describe=validated_data["describe"]
        )

        # 将主任务包的file字段,改成最新的子任务包的file,主任务包file字段展示最新的子版本
        taskpackage.file = taskpackageson.file
        taskpackage.save()

        return taskpackageson


class TaskPackageOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPackageOwner
        fields = ["id", "taskpackage_name", "owner", "exowner", "createtime", "describe"]
        extra_kwargs = {
            "taskpackage_name": {"required": True, "allow_null": False, "help_text": u"主任务包名字"},
            "owner": {"required": True, "allow_null": False, "help_text": u"要@的作业员"},
            "exowner": {"read_only": True},
            "createtime": {"format": '%Y-%m-%d %H:%M:%S'},
        }

    def validate(self, validated_data):
        taskpackage_name = validated_data.get("taskpackage_name")
        try:
            taskpackage = TaskPackage.objects.get(name=taskpackage_name)
        except TaskPackage.DoesNotExist:
            raise serializers.ValidationError(u"任务包{}不存在".format(taskpackage_name))
        else:
            if validated_data["owner"] == taskpackage.owner:
                raise serializers.ValidationError(u"该任务包已经在{}名下".format(validated_data["owner"]))

            validated_data["taskpackage"] = taskpackage
            validated_data["exowner"] = taskpackage.owner

        return validated_data

    def create(self, validated_data):
        taskpackage = validated_data["taskpackage"]
        # del validated_data["taskpackage"]
        # taskpackageowner = super(TaskPackageOwnerSerializer, self).create(validated_data)
        taskpackageowner = TaskPackageOwner.objects.create(
            taskpackage_name=validated_data["taskpackage_name"],
            owner=validated_data["owner"],
            exowner=validated_data["exowner"],
            describe=validated_data["describe"]
        )

        taskpackage.exowner = taskpackage.owner
        taskpackage.owner = validated_data["owner"]
        taskpackage.save()

        return taskpackageowner
