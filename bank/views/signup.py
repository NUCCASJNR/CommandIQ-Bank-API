#!/usr/bin/env python3

"""Contains User Signup View"""

from rest_framework import generics, status
from rest_framework.response import Response
from bank.models.user import User
from bank.serializers.signup import UserSerializer
from bank.utils.email_utils import EmailUtils, RedisClient
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist


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

        if existing_user:
            return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        elif existing_email:
            return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if required fields are present
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not serializer.validated_data.get(field):
                return Response({"message": f"{field} is required to signup"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Generate a verification code
            verification_code = EmailUtils.generate_verification_code()

            # Create the user
            user = User.custom_save(**serializer.validated_data)

            # Send the verification email
            EmailUtils.send_verification_email(user)

            response_data = {
                "message": "User registered successfully. Check your email for the verification code.",
                "username": User.to_dict(user)['username'],
                "email": User.to_dict(user)['email']
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserVerificationView(APIView):
    """
    User Verification View
    """

    def post(self, request, *args, **kwargs):
        """
        Verify a user
        :param request: Request object
        :param args:
        :param kwargs:
        :return: User object in dict format
        """
        verification_code = request.data['verification_code']
        user_id = request.data['user_id']
        redis_client = RedisClient()
        key = f'user_id:{user_id}:{verification_code}'
        required_fields = ['verification_code', 'user_id']
        for field in required_fields:
            if not request.data.get(field):
                return Response({"message": f"{field} is required to verify user"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            code = redis_client.get_key(key)
            if code:
                try:
                    user = User.custom_get(**{'id': user_id, 'verification_code': verification_code})
                    # user.verified = True
                    User.custom_update(filter_kwargs={'id': user_id,
                                                      'verification_code': verification_code},
                                       update_kwargs={'verified': True})
                    redis_client.delete_key(key)
                    response_data = {
                        "message": "Email verification successful",
                        "username": User.to_dict(user)['username'],
                        "email": User.to_dict(user)['email']
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    return Response({"message": "Invalid or expired verification code"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Invalid or expired verification code"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
