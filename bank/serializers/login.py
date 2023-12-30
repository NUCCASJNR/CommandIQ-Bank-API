#!/usr/bin/env python3

from rest_framework import serializers
from bank.models.user import User


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for obtaining an authentication token.
    """
    username = serializers.CharField(label="Username")
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = User.find_obj_by(**{'username': username})
            if user:
                if user.check_password(password):
                    if user.verified:
                        attrs['user'] = user
                        return attrs
                    else:
                        msg = 'Account not verified'
                        raise serializers.ValidationError(msg)
                else:
                    msg = 'Incorrect password'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'User not found'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password"'
            raise serializers.ValidationError(msg)
