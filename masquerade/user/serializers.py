# -*- coding:utf-8 -*-

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'nick_name', 'status', 'create_time')
        read_only_fields = ('create_time',)