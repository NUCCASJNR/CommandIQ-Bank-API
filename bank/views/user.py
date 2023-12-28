#!/usr/bin/env python3

"""Contains User Signup View"""

from rest_framework import generics, status
from rest_framework.response import Response
from bank.models.user import User
from bank.serializers.user import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    User Registration View
    """
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new user
        :param request: Request object
        :param args: Argument
        :param kwargs: Keyword argument
        :return: The created user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.custom_save(**serializer.validated_data)
        response_data = {
            "message": "User registered successfully",
            "username": User.to_dict(user)['username'],
            "email": User.to_dict(user)['email'],
        }
        return Response(response_data, status=status.HTTP_201_CREATED)