#!/usr/bin/env python3

"""Contains User Signup View"""

from rest_framework import generics, status
from rest_framework.response import Response
from bank.models.user import User
from bank.serializers.signup import UserSerializer


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

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        # Check if username or email already exists
        existing_user = User.find_obj_by(username=username)
        existing_email = User.find_obj_by(email=email)

        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not serializer.validated_data.get(field):
                return Response({"message": f"{field} is required to signup"}, status=status.HTTP_400_BAD_REQUEST)
        if existing_user:
            return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        elif existing_email:
            return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the user if it doesn't exist
            user = User.custom_save(**serializer.validated_data)
            response_data = {
                "message": "User registered successfully",
                "username": User.to_dict(user)['username'],
                "email": User.to_dict(user)['email'],
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
