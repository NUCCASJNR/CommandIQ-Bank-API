#!/usr/bin/env python3

"""Contains User Serializer"""

from rest_framework import serializers
from bank.models.user import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer class
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id', 'created_at', 'updated_at')
