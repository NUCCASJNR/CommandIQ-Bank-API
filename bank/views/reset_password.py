#!.usr/bin/env python3
from bank.utils.email_utils import EmailUtils
from django.core.exceptions import ObjectDoesNotExist
from bank.serializers.reset_password import ResetPasswordSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from bank.models.user import User


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
            User.custom_update(filter_kwargs={'email': user_email}, update_kwargs={'reset_token': reset_token})
            response_data = {
                "message": "Reset password token successfully sent",
                "email": User.to_dict(user)['email']
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": 'Incorrect Email Address or Username'}, status=status.HTTP_400_BAD_REQUEST)
