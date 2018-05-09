# -*- coding:utf-8 -*-

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nick_name', 'password', 'status', 'create_time', 'salt')

        write_only_fields = ('username', 'password', 'salt',)
        read_only_fields = ('create_time', 'id',)
        allow_blank_fields = ('status', 'nick_name',)