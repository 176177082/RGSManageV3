# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'isadmin']
        # extra_kwargs = {'password': {"write_only": True}}
        extra_kwargs = {'password': {"write_only": True},'isadmin': {"write_only": True}}

    # 只用来创建测试用户
    def create(self, validated_data):
        user = super(UserListSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["isadmin"]
