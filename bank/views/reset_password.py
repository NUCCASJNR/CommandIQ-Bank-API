#!/usr/bin/env python3

import logging
from bank.utils.email_utils import EmailUtils, RedisClient
from django.core.exceptions import ObjectDoesNotExist
from bank.serializers.reset_password import ResetPasswordSerializer, ResetPasswordConfirmSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from bank.models.user import User

logging.basicConfig(
    filename='reset_password.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s',
)


class ResetPasswordView(APIView):
    """
    Reset password View for sending reset token to user
    """
    def post(self, request, *args, **kwargs):
        """
        Handles POST request for sending reset token to user
        :param request: Request obj
        :param args: AArgument
        :param kwargs: Optional keyword arguments
        :return: Nothing
        """
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        try:
            if '@' in username:
                user = User.custom_get(**{'email': username})
            else:
                user = User.custom_get(**{'username': username})
            reset_token = EmailUtils.generate_verification_code()
            user_email = User.to_dict(user)['email']
            # Send Email to user
            EmailUtils.send_password_reset_email(user, reset_token, user_email)
            logging.info(f'Reset token sent to user: {user_email} : {reset_token}')
            User.custom_update(filter_kwargs={'email': user_email}, update_kwargs={'reset_token': reset_token})
            response_data = {
                "message": "Reset password token successfully sent",
                "email": User.to_dict(user)['email']
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": 'Incorrect Email Address or Username'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(APIView):
    """
    View for confirming the reset password token
    """

    def post(self, request, *args, **kwargs):
        """
        Post request for confirming user request token
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get('token')
        password = serializer.validated_data.get('new_password')
        print(serializer.validated_data)
        try:
            user = User.custom_get(**{'reset_token': token})
            user_id = User.to_dict(user)['id']
            redis_client = RedisClient()
            key = f'reset_token:{user_id}:{token}'
            stored_token = redis_client.get_key(key)

            if stored_token:
                # hashed_pwd = user.set_password(password)
                # user.save()
                User.custom_update(filter_kwargs={'reset_token': token}, update_kwargs={'password': password})

                # delete the token from Redis after it's been used
                redis_client.delete_key(key)

                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid or expired reset token'}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({'message': 'Invalid reset token'}, status=status.HTTP_400_BAD_REQUEST)