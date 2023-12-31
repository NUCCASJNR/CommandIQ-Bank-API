#!/usr/bin/env python3

from rest_framework import serializers
from bank.models.user import User
from django.core.exceptions import ObjectDoesNotExist


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for obtaining an authentication token.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'id', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        """
        Validate and authenticate the user.
        """
        username = data['username']
        password = data['password']
        try:
            if '@' in username:
                user = User.find_obj_by(email=username)
            else:
                user = User.find_obj_by(username=username)

            if user and user.check_password(password):
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError('Invalid username or password')

        except ObjectDoesNotExist:
            raise serializers.ValidationError('User not found')
